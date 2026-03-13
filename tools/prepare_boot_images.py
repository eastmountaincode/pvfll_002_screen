#!/usr/bin/env python3
"""Prepare boot illustration PNGs for the 4.2" e-ink display (400x300, 1-bit).

Loads source illustrations, resizes to fit MAX_HEIGHT, converts to clean 1-bit
black-on-white PNGs ready for direct use by display.py.
"""

from PIL import Image
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_DIR = os.path.join(PROJECT_DIR, "images", "boot")

IMAGES_DIR = os.path.join(PROJECT_DIR, "..", "..", "images", "lylia_illustrations")
BOOT_SPLASH = os.path.join(PROJECT_DIR, "..", "..", "htmlpg-003", "pvfll-003-view", "images", "boot_splash.png")

MAX_HEIGHT = 220
THRESHOLD = 140

ILLUSTRATIONS = [
    ("boot_splash", BOOT_SPLASH),
    ("bees",        os.path.join(IMAGES_DIR, "bees.png")),
    ("butterfly",   os.path.join(IMAGES_DIR, "butterfly.png")),
    ("psychic",     os.path.join(IMAGES_DIR, "psychic.png")),
    ("yoyo",        os.path.join(IMAGES_DIR, "yoyo.png")),
]


def convert_image(path, name):
    raw = Image.open(path)

    # Composite onto white background to handle transparency
    bg = Image.new("RGBA", raw.size, (255, 255, 255, 255))
    if raw.mode == "RGBA":
        bg.paste(raw, mask=raw.split()[3])
    else:
        bg.paste(raw)
    img = bg.convert("L")

    w, h = img.size
    if h > MAX_HEIGHT:
        scale = MAX_HEIGHT / h
        w = int(w * scale)
        h = MAX_HEIGHT
        img = img.resize((w, h), Image.LANCZOS)

    # Threshold to clean 1-bit: dark pixels → black, light → white
    bw = img.point(lambda p: 255 if p >= THRESHOLD else 0, mode='1')

    print(f"  {name}: {w}x{h} (from {path})")
    return bw


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for name, path in ILLUSTRATIONS:
        if not os.path.exists(path):
            print(f"  WARNING: {path} not found, skipping {name}")
            continue
        img = convert_image(path, name)
        out_path = os.path.join(OUTPUT_DIR, f"{name}.png")
        img.save(out_path)
        print(f"  → {out_path}")

    print(f"\nDone. {len(ILLUSTRATIONS)} images written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
