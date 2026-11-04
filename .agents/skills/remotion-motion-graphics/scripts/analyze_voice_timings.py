#!/usr/bin/env python3
"""
Analyze a voiceover WAV file using FFmpeg silencedetect and print a table of
speech segments in seconds and 30fps frames for Remotion synchronization.
"""
import re
import subprocess
import sys
import wave


def analyze_audio(wav_path: str, fps: int = 30, noise_db: int = -28, min_silence: float = 0.15):
    with wave.open(wav_path, 'r') as w:
        duration = w.getnframes() / float(w.getframerate())

    cmd = [
        'ffmpeg', '-i', wav_path,
        '-af', f'silencedetect=noise={noise_db}dB:d={min_silence}',
        '-f', 'null', '-'
    ]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')
    output = proc.stderr

    starts = [float(x) for x in re.findall(r'silence_start:\s*([0-9.]+)', output)]
    ends = [float(x) for x in re.findall(r'silence_end:\s*([0-9.]+)', output)]

    print(f"Total Duration: {duration:.2f}s ({int(round(duration * fps))} frames @ {fps}fps)\n")
    print("| Segment # | Start (s) | End (s) | Start Frame | End Frame | Duration (s) |")
    print("| :--- | :--- | :--- | :--- | :--- | :--- |")

    speech_segments = []
    cursor = 0.0
    for s_start, s_end in zip(starts, ends):
        if s_start - cursor > 0.08:
            speech_segments.append((cursor, s_start))
        cursor = s_end
    if duration - cursor > 0.08:
        speech_segments.append((cursor, duration))

    for idx, (seg_start, seg_end) in enumerate(speech_segments, 1):
        f_start = int(round(seg_start * fps))
        f_end = int(round(seg_end * fps))
        print(f"| {idx:02d} | {seg_start:.2f}s | {seg_end:.2f}s | {f_start} | {f_end} | {seg_end - seg_start:.2f}s |")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_voice_timings.py <path-to-voice.wav>")
        sys.exit(1)
    analyze_audio(sys.argv[1])
