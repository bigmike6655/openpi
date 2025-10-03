"""A tiny terminal animation of a flying hotdog.

Run this module to watch a hotdog take off and soar across your terminal.
The animation relies only on the Python standard library and should work on
any POSIX-compatible terminal that understands ANSI escape codes.
"""
from __future__ import annotations

import itertools
import os
import shutil
import sys
import time
from typing import Sequence

# Frames are rendered by vertically offsetting this ASCII art hotdog.
HOTDOG_ART = (
    "        __====__        ",
    "      .'  .--.  '.      ",
    "     /   /    \   \\",
    "    |   |      |   |",
    "    |   |  --  |   |",
    "     \\   \\____/   /",
    "      '.__'__'__.'",
    "        /  /  \\",
    "       /__/____\\",
)

CLOUD_ART = [
    "      _        _",
    "   _( )__  __( )_",
    " (_   __)(__   _)",
    "   (_)      (_)"
]

CLEAR_SCREEN = "\033[2J\033[H"


def draw_frame(height: int, vertical_offset: int) -> str:
    """Render a single frame of the animation.

    Args:
        height: The total number of rows in the terminal.
        vertical_offset: How far from the top of the screen to place the hotdog.
    """
    # Build an empty canvas filled with spaces.
    width = shutil.get_terminal_size((80, height)).columns
    canvas = [" " * width for _ in range(height)]

    def blit(sprite: Sequence[str], top: int, left: int) -> None:
        for row_idx, line in enumerate(sprite):
            y = top + row_idx
            if 0 <= y < height:
                line = line[: len(canvas[y])]
                row = list(canvas[y])
                for x, char in enumerate(line):
                    if 0 <= left + x < len(row) and char != " ":
                        row[left + x] = char
                canvas[y] = "".join(row)

    cloud_spacing = height // 4
    for cloud_idx in range(4):
        offset = (cloud_idx * cloud_spacing + vertical_offset // 2) % height
        blit(CLOUD_ART, offset, 2 + (cloud_idx % 2) * 12)

    blit(HOTDOG_ART, vertical_offset, max(0, width // 2 - 10))
    return "\n".join(canvas)


def animate(duration: float = 6.0, fps: float = 12.0) -> None:
    """Animate the flying hotdog for the requested duration."""
    if sys.platform == "win32":
        os.system("")

    frame_delay = 1.0 / fps
    start_time = time.perf_counter()
    terminal_height = shutil.get_terminal_size((80, 24)).lines

    for _ in itertools.count():
        elapsed = time.perf_counter() - start_time
        if elapsed > duration:
            break

        vertical_offset = terminal_height - 1 - int((elapsed / duration) * (terminal_height + len(HOTDOG_ART)))
        print(CLEAR_SCREEN + draw_frame(terminal_height, vertical_offset), flush=True, end="")
        time.sleep(max(0.0, frame_delay - (time.perf_counter() - start_time - elapsed)))

    print(CLEAR_SCREEN + "The hotdog has flown beyond the horizon! 🌭✈️")


if __name__ == "__main__":
    try:
        animate()
    except KeyboardInterrupt:
        print("\nFlight aborted. See you next time!", file=sys.stderr)
