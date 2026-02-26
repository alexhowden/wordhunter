# ============================================================
# COORDINATES
# ============================================================
# Run `python tools/get_coords.py` to get coordinates.
# Hover over each element — a live GUI shows x, y.
# ============================================================

# (x, y) of the "Play" / "Start" button on the Word Hunt screen.
# The bot clicks this before the round begins.
START_BUTTON = (227, 815)

# Word Hunt is a 4x4 letter grid.
# Layout (row, col):
#   [0,0] [0,1] [0,2] [0,3]
#   [1,0] [1,1] [1,2] [1,3]
#   [2,0] [2,1] [2,2] [2,3]
#   [3,0] [3,1] [3,2] [3,3]
GRID_COORDS = [
    [(105, 615), (185, 615), (265, 615), (345, 615)],   # row 0
    [(105, 695), (185, 695), (265, 695), (345, 695)],   # row 1
    [(105, 775), (185, 775), (265, 775), (345, 775)],   # row 2
    [(105, 855), (185, 855), (265, 855), (345, 855)],   # row 3
]

# Duration (seconds) of the swipe between each letter.
# Lower = faster, but too fast may miss inputs.
SWIPE_DURATION = 0.04

# Seconds to pause between playing each word.
WORD_PAUSE = 0.1

# Seconds to wait after clicking Start before scanning the board.
COUNTDOWN_WAIT = 1.0

# How long each Word Hunt round lasts (seconds).
ROUND_DURATION = 80
