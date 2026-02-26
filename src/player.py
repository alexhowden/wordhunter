"""
player.py — Automates mouse input to play Word Hunt via iPhone Mirroring.

Uses Quartz CoreGraphics to emit proper kCGEventLeftMouseDragged events.
pyautogui.moveTo() while held only fires mouseMoved, not mouseDragged —
iPhone Mirroring ignores those and never registers a touch drag.
"""

import time
import Quartz
from src.board import Board
from config.coordinates import SWIPE_DURATION, WORD_PAUSE

_BUTTON = Quartz.kCGMouseButtonLeft


def _post(event_type: int, x: int, y: int) -> None:
    """Post a single CoreGraphics mouse event at logical screen coords (x, y)."""
    event = Quartz.CGEventCreateMouseEvent(None, event_type, (x, y), _BUTTON)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def _move_dragging(x1: int, y1: int, x2: int, y2: int, duration: float, steps: int = 20) -> None:
    """
    Interpolate from (x1,y1) to (x2,y2) firing kCGEventLeftMouseDragged at
    each step. This is what iPhone Mirroring needs to recognise a touch drag.
    """
    for i in range(1, steps + 1):
        t = i / steps
        ix = int(x1 + (x2 - x1) * t)
        iy = int(y1 + (y2 - y1) * t)
        _post(Quartz.kCGEventLeftMouseDragged, ix, iy)
        time.sleep(duration / steps)


class Player:
    def __init__(self, board: Board):
        self.board = board

    def play_word(self, path: list[tuple[int, int]]) -> None:
        if not path:
            return

        coords = [self.board.coord_at(r, c) for r, c in path]

        # Press down on the first letter
        _post(Quartz.kCGEventLeftMouseDown, coords[0][0], coords[0][1])
        time.sleep(0.05)

        # Drag through each subsequent letter
        for i in range(1, len(coords)):
            x1, y1 = coords[i - 1]
            x2, y2 = coords[i]
            _move_dragging(x1, y1, x2, y2, SWIPE_DURATION)

        # Release
        _post(Quartz.kCGEventLeftMouseUp, coords[-1][0], coords[-1][1])
        time.sleep(WORD_PAUSE)

    def play_all(self, results: list[tuple[str, list[tuple[int, int]]]], deadline: float | None = None) -> None:
        """
        Play words until the list is exhausted or deadline (time.time()) is reached.
        """
        print(f"\nPlaying {len(results)} words...")

        for i, (word, path) in enumerate(results, 1):
            if deadline and time.time() >= deadline:
                print(f"  Time's up — stopped after {i - 1} words.")
                return
            print(f"  [{i}] {word} ({len(word)} letters)")
            self.play_word(path)

        print("Done.")
