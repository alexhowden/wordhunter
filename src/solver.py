"""
solver.py — Finds all valid words in the Word Hunt grid using a Trie + DFS.

Word Hunt rules (same as Boggle):
  - Letters must be adjacent (including diagonals).
  - Each cell can only be used once per word.
  - Minimum word length is 3.
"""

from __future__ import annotations
from src.board import Board

WORDLIST_PATH = "data/wordlist.txt"
MIN_WORD_LENGTH = 3

# Adjacency directions: all 8 neighbours
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              ( 0, -1),           ( 0, 1),
              ( 1, -1), ( 1, 0), ( 1, 1)]


# ---------------------------------------------------------------------------
# Trie
# ---------------------------------------------------------------------------

class TrieNode:
    __slots__ = ("children", "is_word")

    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def load_wordlist(self, path: str) -> None:
        with open(path, "r") as f:
            for line in f:
                word = line.strip().upper()
                if len(word) >= MIN_WORD_LENGTH and word.isalpha():
                    self.insert(word)
        print(f"Wordlist loaded from {path}")


# ---------------------------------------------------------------------------
# Solver
# ---------------------------------------------------------------------------

class Solver:
    def __init__(self, board: Board, trie: Trie):
        self.board = board
        self.trie = trie

    def solve(self) -> list[tuple[str, list[tuple[int, int]]]]:
        """
        Returns a list of (word, path) tuples sorted by word length descending.
        path is a list of (row, col) indices.
        """
        found: dict[str, list[tuple[int, int]]] = {}
        visited = [[False] * 4 for _ in range(4)]

        for r in range(4):
            for c in range(4):
                self._dfs(r, c, self.trie.root, "", [], visited, found)

        # Sort longest words first (highest scoring in Word Hunt)
        results = sorted(found.items(), key=lambda x: len(x[0]), reverse=True)
        return results

    def _dfs(
        self,
        row: int,
        col: int,
        node: TrieNode,
        current_word: str,
        path: list[tuple[int, int]],
        visited: list[list[bool]],
        found: dict[str, list[tuple[int, int]]],
    ) -> None:
        letter = self.board.letter_at(row, col)
        child = node.children.get(letter)
        if child is None:
            return  # No words down this branch

        current_word += letter
        path.append((row, col))
        visited[row][col] = True

        if child.is_word and current_word not in found:
            found[current_word] = list(path)

        for dr, dc in DIRECTIONS:
            nr, nc = row + dr, col + dc
            if 0 <= nr < 4 and 0 <= nc < 4 and not visited[nr][nc]:
                self._dfs(nr, nc, child, current_word, path, visited, found)

        path.pop()
        visited[row][col] = False
