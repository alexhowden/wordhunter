"""
board.py — Represents the 4x4 Word Hunt letter grid.
"""


class Board:
    """Holds the 16 letters in a 4x4 grid and their screen coordinates."""

    def __init__(self, letters: list[list[str]], coords: list[list[tuple[int, int]]]):
        """
        Args:
            letters: 4x4 list of single uppercase letters, e.g.
                     [['A','B','C','D'], ['E','F','G','H'], ...]
            coords:  4x4 list of (x, y) screen coords matching each letter cell.
        """
        if len(letters) != 4 or any(len(row) != 4 for row in letters):
            raise ValueError("letters must be a 4x4 grid")
        if len(coords) != 4 or any(len(row) != 4 for row in coords):
            raise ValueError("coords must be a 4x4 grid")

        self.letters = [[c.upper() for c in row] for row in letters]
        self.coords = coords

    def letter_at(self, row: int, col: int) -> str:
        return self.letters[row][col]

    def coord_at(self, row: int, col: int) -> tuple[int, int]:
        return self.coords[row][col]

    def display(self) -> None:
        """Pretty-print the board to stdout."""
        print("\nBoard:")
        for row in self.letters:
            print("  " + "  ".join(row))
        print()
