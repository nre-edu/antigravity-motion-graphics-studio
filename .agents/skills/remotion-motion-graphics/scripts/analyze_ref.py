#!/usr/bin/env python3
"""
Measure a reference video or still image(s) so its visual style and pacing can be matched in Remotion.
Adapted from arabic-motion (by Dr. Mohamed Refat - nre-edu) for Antigravity Remotion Studio.

Usage:
  python .agents/skills/remotion-motion-graphics/scripts/analyze_ref.py <reference-dir> [--out <output-dir>]
"""
import argparse
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}
STILL = {".png", ".jpg", ".jpeg", ".webp"}


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace", **kw)


def probe(ffprobe, path):
    out = run([
        ffprobe, "-v", "error",
        "-show_entries", "stream=codec_type,width,height,r_frame_rate:format=duration",
        "-of", "json", str(path)
    ])
    data = json.loads(out.stdout)
    v = next(s for s in data["streams"] if s["codec_type"] == "video")
    num, den = (int(x) for x in v["r_frame_rate"].split("/"))
    return {
        "width": v["width"],
        "height": v["height"],
        "fps": round(num / den, 2),
        "duration": float(data["format"]["duration"]),
        "has_audio": any(s["codec_type"] == "audio" for s in data["streams"]),
    }


def scene_scores(ffmpeg, path):
    err = run([
        ffmpeg, "-hide_banner", "-i", str(path),
        "-vf", "scale=320:-2,select='gte(scene,0)',metadata=print:key=lavfi.scene_score",
        "-an", "-f", "null", "-"
    ]).stderr
    times = [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)]
    scores = [float(x) for x in re.findall(r"lavfi\.scene_score=([\d.]+)", err)]
    return list(zip(times, scores))


def grab(ffmpeg, path, t, out, width=360):
    run([
        ffmpeg, "-y", "-loglevel", "error",
        "-ss", f"{t:.3f}", "-i", str(path),
        "-frames:v", "1", "-vf", f"scale={width}:-2", "-q:v", "3", str(out)
    ])


def sheet(ffmpeg, frames_glob_dir, prefix, count, out, cols=6):
    rows = max(1, math.ceil(count / cols))
    run([
        ffmpeg, "-y", "-loglevel", "error",
        "-i", str(frames_glob_dir / f"{prefix}-%02d.jpg"),
        "-vf", f"tile={cols}x{rows}:padding=6:color=0x111111",
        "-frames:v", "1", "-q:v", "3", str(out)
    ])


def palette(ffmpeg, sources, top=6):
    counts = Counter()
    sums = {}
    for path, t in sources:
        seek = ["-ss", f"{t:.3f}"] if t is not None else []
        raw = subprocess.run([
            ffmpeg, "-loglevel", "error", *seek, "-i", str(path),
            "-frames:v", "1", "-vf", "scale=48:48",
            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"
        ], capture_output=True).stdout
        for i in range(0, len(raw) - 2, 3):
            px = (raw[i], raw[i + 1], raw[i + 2])
            key = (px[0] >> 4, px[1] >> 4, px[2] >> 4)
            counts[key] += 1
            s = sums.setdefault(key, [0, 0, 0])
            for k in range(3):
                s[k] += px[k]
    total = sum(counts.values()) or 1
    out = []
    for key, c in counts.most_common(40):
        rgb = tuple(round(v / c) for v in sums[key])
        if all(sum((x - y) ** 2 for x, y in zip(rgb, o["rgb"])) > 2500 for o in out):
            out.append({"hex": "#%02x%02x%02x" % rgb, "rgb": rgb, "share": round(c / total, 3)})
        if len(out) == top:
            break
    return [{"hex": o["hex"], "share": o["share"]} for o in out]


def aspect(w, h):
    return "vertical" if h > w * 1.05 else "horizontal" if w > h * 1.05 else "square"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ref_dir", nargs="?", default="reference", help="Path to reference folder")
    ap.add_argument("--threshold", type=float, default=0.3)
    ap.add_argument("--out", default=None, help="Output directory (defaults to <ref_dir>/analysis)")
    a = ap.parse_args()

    ref = Path(a.ref_dir)
    if not ref.is_dir():
        sys.exit(f"Reference folder not found: {ref}")

    out = Path(a.out) if a.out else (ref / "analysis")
    frames = out / "frames"
    if frames.exists():
        shutil.rmtree(frames)
    frames.mkdir(parents=True, exist_ok=True)

    videos = sorted(p for p in ref.glob("*") if p.suffix.lower() in VIDEO)
    stills = sorted(p for p in ref.glob("*") if p.suffix.lower() in STILL and "contact-sheet" not in p.name)
    if not videos and not stills:
        sys.exit("No reference video or images found in reference folder.")

    ffmpeg = os.environ.get("AM_FFMPEG", "ffmpeg")
    ffprobe = os.environ.get("AM_FFPROBE", "ffprobe")

    analysis = {"sheets": {}}
    sources = []

    if videos:
        video = videos[0]
        info = probe(ffprobe, video)
        scores = scene_scores(ffmpeg, video)
        cuts = [t for t, s in scores if s >= a.threshold and t > 0.2]
        bounds = [0.0] + cuts + [info["duration"]]
        shots = [round(b - a, 2) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
        mids = [(x + y) / 2 for x, y in zip(bounds, bounds[1:])][:24]

        for i, t in enumerate(mids, 1):
            grab(ffmpeg, video, t, frames / f"shot-{i:02d}.jpg")
        sheet(ffmpeg, frames, "shot", len(mids), out / "shots.jpg", cols=min(6, max(1, len(mids))))

        opening = [t / 2 for t in range(0, 7) if t / 2 < info["duration"]]
        for i, t in enumerate(opening, 1):
            grab(ffmpeg, video, t, frames / f"open-{i:02d}.jpg")
        sheet(ffmpeg, frames, "open", len(opening), out / "opening.jpg", cols=max(1, len(opening)))

        step = 0.5 if info["duration"] <= 24 else 1.0
        rows = max(1, math.ceil(info["duration"] / step / 8))
        run([
            ffmpeg, "-y", "-loglevel", "error", "-i", str(video),
            "-vf", f"fps={1 / step},scale=240:-2,tile=8x{rows}:padding=4:color=0x111111",
            "-frames:v", "1", "-q:v", "3", str(out / "timeline.jpg")
        ])

        analysis["video"] = {"file": video.name, **info, "aspect": aspect(info["width"], info["height"])}
        analysis["cuts"] = [round(c, 2) for c in cuts]
        analysis["shots"] = len(shots)
        analysis["shot_length"] = {
            "mean": round(statistics.mean(shots), 2),
            "median": round(statistics.median(shots), 2),
            "min": min(shots),
            "max": max(shots),
        } if shots else None
        analysis["cuts_per_10s"] = round(len(cuts) / info["duration"] * 10, 1)
        analysis["sheets"] = {
            "shots": (out / "shots.jpg").as_posix(),
            "opening": (out / "opening.jpg").as_posix(),
            "timeline": (out / "timeline.jpg").as_posix(),
        }
        sources.extend((video, t) for t in mids[:12])

    analysis["palette"] = palette(ffmpeg, sources) if sources else []
    if frames.exists():
        shutil.rmtree(frames)

    (out / "analysis.json").write_text(json.dumps(analysis, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(analysis, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
