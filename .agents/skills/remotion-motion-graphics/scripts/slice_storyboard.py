#!/usr/bin/env python3
"""
Slice a multi-panel storyboard grid image (e.g. 4x2, 3x2, 2x2) into individual
high-resolution scene PNG files for Remotion motion graphics cards.

Usage:
  python slice_storyboard.py <storyboard.png> <output_dir> [--cols 4] [--rows 2]
"""
import argparse
import os
import sys
from PIL import Image


def slice_storyboard(image_path: str, output_dir: str, cols: int = 4, rows: int = 2):
    if not os.path.exists(image_path):
        sys.exit(f"Storyboard image not found: {image_path}")

    os.makedirs(output_dir, exist_ok=True)
    img = Image.open(image_path)
    w, h = img.size

    col_w = w / float(cols)
    row_h = h / float(rows)
    total_panels = cols * rows

    print(f"Slicing {image_path} ({w}x{h}) into {cols}x{rows} = {total_panels} panels...")

    out_paths = []
    for idx in range(total_panels):
        col = idx % cols
        row = idx // cols
        left = int(round(col * col_w))
        top = int(round(row * row_h))
        right = int(round((col + 1) * col_w))
        bottom = int(round((row + 1) * row_h))

        panel = img.crop((left, top, right, bottom))
        filename = f"scene-{(idx + 1):02d}.png"
        out_path = os.path.join(output_dir, filename)
        panel.save(out_path, format="PNG")
        out_paths.append(out_path)
        print(f"  [+] Saved {filename} ({right - left}x{bottom - top}px)")

    print(f"Successfully saved {len(out_paths)} scene images into: {output_dir}")
    return out_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slice storyboard sheet into scene assets")
    parser.add_argument("image", help="Path to storyboard image file")
    parser.add_argument("out_dir", nargs="?", default="scenes", help="Directory to save sliced scenes")
    parser.add_argument("--cols", type=int, default=4, help="Number of columns in grid (default: 4)")
    parser.add_argument("--rows", type=int, default=2, help="Number of rows in grid (default: 2)")
    args = parser.parse_args()

    slice_storyboard(args.image, args.out_dir, args.cols, args.rows)
