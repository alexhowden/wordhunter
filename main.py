"""
main.py — Entry point for the Word Hunt bot.

Usage:
    python main.py

Flow:
    1. Click the Start button in Word Hunt (iPhone Mirroring).
    2. Wait for the game countdown to finish.
    3. Screenshot and OCR the board to detect letters.
    4. Solve for all valid words.
    5. Auto-play them via mouse automation.
"""

import time
import pyautogui
from src.board import Board
from src.solver import Solver, Trie
from src.player import Player
from src.scanner import scan_board
from config.coordinates import GRID_COORDS, START_BUTTON, COUNTDOWN_WAIT, ROUND_DURATION

WORDLIST_PATH = "data/wordlist.txt"

# Safety: abort if mouse is moved to a screen corner
pyautogui.FAILSAFE = True


def main():
    print("=== Word Hunt Bot ===\n")
    print("Clicking Start in 3 seconds — switch to iPhone Mirroring now!")
    time.sleep(3)

    # 1. Click Start and record when the round began
    pyautogui.doubleClick(START_BUTTON[0], START_BUTTON[1])
    round_start = time.time()

    # 2. Brief pause then scan
    time.sleep(COUNTDOWN_WAIT)
    grid = scan_board()

    # 3. Print detected board
    print("\nDetected board:")
    for row in grid:
        print("  " + "  ".join(row))
    print()

    # 4. Build board + solve
    board = Board(grid, GRID_COORDS)
    trie = Trie()
    trie.load_wordlist(WORDLIST_PATH)
    solver = Solver(board, trie)
    results = solver.solve()
    print(f"Found {len(results)} words.")

    if not results:
        print("No words found.")
        return

    # 5. Play until the round timer runs out
    deadline = round_start + ROUND_DURATION
    player = Player(board)
    player.play_all(results, deadline=deadline)


if __name__ == "__main__":
    main()
