"""
tools/get_coords.py — Live GUI overlay showing the current mouse position.

Usage:
    python tools/get_coords.py

A small window will appear showing x, y, and the pixel colour under
your cursor in real time. Hover over each cell/button you need and
copy the coordinates into config/coordinates.py.
Press Ctrl+C in the terminal to stop.
"""

import pyautogui

print("GUI coordinate display running — hover over any element to see its position.")
print("Press Ctrl+C to stop.\n")
pyautogui.displayMousePosition()
