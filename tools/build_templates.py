"""
tools/build_templates.py — One-time setup to build the letter template library.

Usage:
    1. Open iPhone Mirroring with Word Hunt showing a board (any board works).
    2. Run: python tools/build_templates.py
    3. Look at the board and type all 16 letters left-to-right, top-to-bottom.
    4. Templates are saved to templates/<letter>.png  (overwrites existing).

You only need to do this once per new letter. Existing templates are kept.
"""

import os
import sys
import pyautogui
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config.coordinates import GRID_COORDS

TEMPLATES_DIR = "templates"
CELL_RADIUS = 28  # keep in sync with scanner.py


def _get_retina_scale(screenshot: Image.Image) -> float:
    logical_w, _ = pyautogui.size()
    return screenshot.width / logical_w


def _crop_cell(screenshot: Image.Image, cx: int, cy: int, scale: float) -> Image.Image:
    pcx = int(cx * scale)
    pcy = int(cy * scale)
    r   = int(CELL_RADIUS * scale)
    return screenshot.crop((pcx - r, pcy - r, pcx + r, pcy + r))


def main():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    print("Taking screenshot...")
    screenshot = pyautogui.screenshot()
    scale = _get_retina_scale(screenshot)
    print(f"Retina scale: {scale:.2f}×\n")

    ref_path = os.path.join(TEMPLATES_DIR, "_board_reference.png")
    screenshot.save(ref_path)
    print(f"Board reference saved to {ref_path}\n")

    print("Look at the Word Hunt board (left-to-right, top-to-bottom).")
    print("Type all 16 letters with no spaces, then press Enter.")
    print("Example: ABCDEFGHIJKLMNOP\n")

    while True:
        raw = input("16 letters: ").strip().upper().replace(" ", "")
        if len(raw) == 16 and raw.isalpha():
            break
        print(f"  Got {len(raw)} characters — need exactly 16 letters. Try again.")

    # Match each letter to its cell crop and save
    cells = [(row_idx, col_idx, cx, cy)
             for row_idx, row in enumerate(GRID_COORDS)
             for col_idx, (cx, cy) in enumerate(row)]

    for (row_idx, col_idx, cx, cy), letter in zip(cells, raw):
        crop = _crop_cell(screenshot, cx, cy, scale)
        out_path = os.path.join(TEMPLATES_DIR, f"{letter}.png")
        crop.save(out_path)
        print(f"  ({row_idx},{col_idx}) → '{letter}'  saved to {out_path}")

    print(f"\nDone.")

    in_library = {
        os.path.splitext(f)[0].upper()
        for f in os.listdir(TEMPLATES_DIR)
        if f.endswith(".png") and len(os.path.splitext(f)[0]) == 1 and os.path.splitext(f)[0].isalpha()
    }
    print(f"Library now contains ({len(in_library)}/26): {' '.join(sorted(in_library))}")
    missing = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ") - in_library
    if missing:
        print(f"Not yet in library: {' '.join(sorted(missing))} — will be added on future boards.")
    else:
        print("All 26 letters are in the library!")


if __name__ == "__main__":
    main()
