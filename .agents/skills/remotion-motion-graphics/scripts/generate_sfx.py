#!/usr/bin/env python3
"""
Procedural Sound Effects (SFX) & Ambient Tech Pad generator for Remotion videos.
Generates a 44.1kHz WAV track containing:
- Subtle warm ambient tech chord pad
- Scene transition whooshes
- UI element pop accents
- Digital counter ticks
- Keyboard typing clicks
- Punchy bullseye / finale impact hit
"""
import json
import math
import random
import struct
import sys
import wave


def generate_sfx_track(
    output_path: str,
    duration: float,
    whooshes: list[float],
    pops: list[float],
    counter_start: float | None = None,
    typing_start: float | None = None,
    impact_time: float | None = None,
    sr: int = 44100,
):
    n_samples = int(sr * duration)
    buf = [0.0] * n_samples

    def add_pop(start, freq0=360, freq1=740, dur=0.065, amp=0.07):
        s0 = int(start * sr)
        n = int(dur * sr)
        phase = 0.0
        for i in range(n):
            idx = s0 + i
            if 0 <= idx < n_samples:
                t = i / sr
                prog = t / dur
                f = freq0 + (freq1 - freq0) * (prog ** 0.6)
                phase += 2 * math.pi * f / sr
                env = math.sin(math.pi * prog) ** 0.8
                buf[idx] += amp * env * math.sin(phase)

    def add_whoosh(start, dur=0.30, amp=0.075):
        s0 = int(start * sr)
        n = int(dur * sr)
        random.seed(int(start * 100))
        lp = 0.0
        for i in range(n):
            idx = s0 + i
            if 0 <= idx < n_samples:
                t = i / sr
                prog = t / dur
                env = math.sin(math.pi * prog) ** 1.5
                alpha = 0.04 + 0.18 * math.sin(math.pi * prog)
                noise = random.uniform(-1.0, 1.0)
                lp = lp + alpha * (noise - lp)
                tone = math.sin(2 * math.pi * (140 + 180 * prog) * t) * 0.4
                buf[idx] += amp * env * (lp * 1.4 + tone)

    def add_impact(start, dur=0.45, amp=0.16):
        s0 = int(start * sr)
        n = int(dur * sr)
        phase = 0.0
        for i in range(n):
            idx = s0 + i
            if 0 <= idx < n_samples:
                t = i / sr
                f = 55 + 190 * math.exp(-t * 28)
                phase += 2 * math.pi * f / sr
                env = math.exp(-t * 8.5)
                buf[idx] += amp * env * math.sin(phase)

    # 1. Subtle warm tech ambient pad
    for i in range(n_samples):
        t = i / sr
        fade = 1.0
        if t < 1.0:
            fade = t / 1.0
        elif t > duration - 1.5:
            fade = max(0.0, (duration - t) / 1.5)
        pulse = 0.75 + 0.25 * math.sin(2 * math.pi * 0.5 * t)
        val = (
            0.45 * math.sin(2 * math.pi * 110.0 * t)
            + 0.25 * math.sin(2 * math.pi * 164.81 * t)
            + 0.20 * math.sin(2 * math.pi * 220.0 * t)
            + 0.10 * math.sin(2 * math.pi * 277.18 * t)
        )
        buf[i] += 0.022 * fade * pulse * val

    # 2. Scene Whooshes
    for ws in whooshes:
        add_whoosh(ws)

    # 3. UI Pops
    for ps in pops:
        add_pop(ps)

    # 4. Counter ticks
    if counter_start is not None:
        for k in range(6):
            add_pop(counter_start + k * 0.11, freq0=800, freq1=1200, dur=0.025, amp=0.06)

    # 5. Typing clicks
    if typing_start is not None:
        for k in range(11):
            add_pop(typing_start + k * 0.09, freq0=1100, freq1=600, dur=0.018, amp=0.045)

    # 6. Bullseye Impact
    if impact_time is not None:
        add_impact(impact_time)
        add_pop(impact_time + 0.02, freq0=520, freq1=1040, dur=0.09, amp=0.09)

    with wave.open(output_path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        data = bytearray()
        for s in buf:
            clamped = max(-0.95, min(0.95, s))
            data.extend(struct.pack('<h', int(clamped * 32767)))
        w.writeframes(bytes(data))
    print(f"Generated {output_path} ({duration:.2f}s) successfully.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_sfx.py <output.wav> <duration_sec> [config_json]")
        sys.exit(1)
    out_wav = sys.argv[1]
    dur = float(sys.argv[2])
    cfg = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    generate_sfx_track(
        output_path=out_wav,
        duration=dur,
        whooshes=cfg.get("whooshes", [0.2, dur * 0.25, dur * 0.5, dur * 0.75]),
        pops=cfg.get("pops", []),
        counter_start=cfg.get("counter_start"),
        typing_start=cfg.get("typing_start"),
        impact_time=cfg.get("impact_time"),
    )
