"""
scanner.py — Captures the Word Hunt board and matches letters via template matching.

Uses OpenCV normalized cross-correlation against a library of known letter crops.
Build the template library once with: python tools/build_templates.py

Retina / HiDPI note:
    pyautogui reports coordinates in LOGICAL pixels (points), but screenshots
    are captured at PHYSICAL pixel resolution (2× on Retina). This module
    auto-detects the scale factor and applies it so crops line up correctly.
"""

import os
import sys
from datetime import datetime

import cv2
import numpy as np
import pyautogui
from PIL import Image

from config.coordinates import GRID_COORDS

# Folder where debug cell images are saved (created automatically).
DEBUG_DIR = "debug"

# Folder containing A.png … Z.png reference crops.
TEMPLATES_DIR = "templates"

# Radius in LOGICAL pixels around each cell center.
CELL_RADIUS = 28


def _get_retina_scale(screenshot: Image.Image) -> float:
    logical_w, _ = pyautogui.size()
    return screenshot.width / logical_w


def _crop_cell(screenshot: Image.Image, cx: int, cy: int, scale: float) -> Image.Image:
    pcx = int(cx * scale)
    pcy = int(cy * scale)
    r   = int(CELL_RADIUS * scale)
    return screenshot.crop((pcx - r, pcy - r, pcx + r, pcy + r))


def _load_templates() -> dict[str, np.ndarray]:
    """
    Load all letter templates from TEMPLATES_DIR as grayscale numpy arrays,
    resized to a canonical size so all comparisons are apples-to-apples.
    """
    templates = {}
    for fname in os.listdir(TEMPLATES_DIR):
        name, ext = os.path.splitext(fname)
        if ext.lower() == ".png" and len(name) == 1 and name.isalpha():
            path = os.path.join(TEMPLATES_DIR, fname)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                templates[name.upper()] = img
    return templates


def _match_letter(crop: Image.Image, templates: dict[str, np.ndarray]) -> tuple[str, float]:
    """
    Compare a cell crop against all templates using normalized cross-correlation.
    Returns (best_letter, score). Score is 0.0–1.0; higher = better match.
    """
    # Convert crop to grayscale numpy array
    cell_gray = cv2.cvtColor(np.array(crop), cv2.COLOR_RGB2GRAY)

    best_letter = "?"
    best_score  = -1.0

    for letter, tmpl in templates.items():
        # Resize template to match cell size for fair comparison
        tmpl_resized = cv2.resize(tmpl, (cell_gray.shape[1], cell_gray.shape[0]),
                                  interpolation=cv2.INTER_AREA)
        result = cv2.matchTemplate(cell_gray, tmpl_resized, cv2.TM_CCOEFF_NORMED)
        score = float(result.max())
        if score > best_score:
            best_score  = score
            best_letter = letter

    return best_letter, best_score


def scan_board(save_debug: bool = False) -> list[list[str]]:
    """
    Take a screenshot and identify each of the 16 grid cells via template matching.

    Args:
        save_debug: If True, saves cell crops to debug/<timestamp>/ for verification.

    Returns a 4x4 list of single uppercase letters.
    """
    if not os.path.isdir(TEMPLATES_DIR) or not os.listdir(TEMPLATES_DIR):
        print("ERROR: No templates found. Run: python tools/build_templates.py")
        sys.exit(1)

    templates = _load_templates()
    print(f"Loaded {len(templates)} letter templates: {' '.join(sorted(templates))}")

    print("Scanning board...", flush=True)
    screenshot = pyautogui.screenshot()

    scale = _get_retina_scale(screenshot)
    print(f"  Retina scale: {scale:.2f}×  "
          f"(logical {pyautogui.size()} → physical {screenshot.size})")

    debug_dir = None
    if save_debug:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        debug_dir = os.path.join(DEBUG_DIR, timestamp)
        os.makedirs(debug_dir, exist_ok=True)
        screenshot.save(os.path.join(debug_dir, "_full_screenshot.png"))

    grid: list[list[str]] = []
    low_confidence: list[str] = []

    for row_idx, row in enumerate(GRID_COORDS):
        row_letters: list[str] = []
        for col_idx, (cx, cy) in enumerate(row):
            crop = _crop_cell(screenshot, cx, cy, scale)
            letter, score = _match_letter(crop, templates)

            if score < 0.6:
                low_confidence.append(
                    f"  cell ({row_idx},{col_idx}) → '{letter}' (score {score:.2f}) — low confidence"
                )

            if debug_dir:
                tag = f"cell_{row_idx}_{col_idx}_{letter}_score{score:.2f}"
                crop.save(os.path.join(debug_dir, f"{tag}.png"))

            row_letters.append(letter)
        grid.append(row_letters)

    if save_debug:
        print(f"Debug images saved → {debug_dir}/")

    if low_confidence:
        print("WARNING: Low-confidence matches (consider re-running build_templates.py):")
        for msg in low_confidence:
            print(msg)
        print()

    return grid
