import time
import sys
import os
import shutil

from typing import List, Tuple, Optional, Set
from src.themes import Theme, DEFAULT_THEME
from maze.structs import Cell

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8


class MazeRenderer:
    """ASCII maze renderer with path 'draw-in' animation"""

    def __init__(
        self,
        maze: List[List[int]],
        cells: List[Cell],
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        path: Optional[List[Tuple[int, int]]] = None,
        theme: Theme = DEFAULT_THEME,
    ) -> None:
        self.maze = maze
        self.cells = cells
        self.entry = entry
        self.exit = exit_
        self.path = path
        self.theme = theme
        self.cell_lookup = {(c.x, c.y): c for c in self.cells}

    def _build_static_lines(
            self, reveal_path: Optional[Set[Tuple[int, int]]] = None
    ) -> List[str]:
        if not self.maze or not self.maze[0]:
            return ["Empty maze"]

        height = len(self.maze)
        width = len(self.maze[0])
        output: list[str] = []

        top = f"{self.theme.WALL}+"
        for x in range(width):
            if self.maze[0][x] & NORTH:
                top += "---+"
            else:
                top += "   +"
        output.append(top)

        for y in range(height):

            if self.maze[y][0] & WEST:
                middle = f"{self.theme.WALL}|"
            else:
                middle = " "
            bottom = f"{self.theme.WALL}+"

            for x in range(width):
                cell = self.maze[y][x]

                cobj = self.cell_lookup.get((x, y))
                is_active = bool(cobj and cobj.is_active)

                if not is_active:
                    content = f"{self.theme.INACTIVE}0{self.theme.RESET}"
                else:
                    content = " "
                    if (x, y) == self.entry:
                        content = f"{self.theme.ENTRY}S{self.theme.RESET}"
                    elif (x, y) == self.exit:
                        content = f"{self.theme.EXIT}E{self.theme.RESET}"
                    elif reveal_path is not None and (x, y) in reveal_path:
                        content = f"{self.theme.PATH}X{self.theme.RESET}"

                if cell & EAST:
                    middle += (
                        f" {content} {self.theme.WALL}|{self.theme.RESET}"
                    )
                else:
                    middle += f" {content}  "

                if cell & SOUTH:
                    bottom += "---+"
                else:
                    bottom += "   +"

            output.append(middle)
            output.append(bottom)

        output.append(self.theme.RESET)
        return output

    def _required_size(self) -> int:
        """Return required terminal columns to render the maze fully."""
        width = len(self.maze[0])
        # top border: starting '+' plus 4 chars per cell
        cols = 1 + width * 4
        return cols

    def _supports_cursor(self) -> bool:
        """Return whether output is on actual TTY and
        whether TTY can support cursor/clear ANSI animation."""
        if not sys.stdout.isatty():
            return False
        term = os.getenv("TERM", "")
        if term == "" or term.lower() == "dumb":
            return False
        return True

    def render(self) -> None:
        """Render maze. Print/animate frames to stdout; no return value."""
        if not self.maze or not self.maze[0]:
            out = "Empty maze"
            sys.stdout.write(out + "\n")
            sys.stdout.flush()
            return

        # If path is None -> never reveal path; print static maze
        if self.path is None:
            final = "\n".join(self._build_static_lines(reveal_path=set()))
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return

        # If terminal doesn't support cursor ops fallback to static final path
        supports_cursor = self._supports_cursor()
        if not supports_cursor:
            final = "\n".join(
                self._build_static_lines(reveal_path=set(self.path))
            )
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return

        # Check terminal width before drawing (only if printing to TTY)
        if sys.stdout.isatty():
            req_cols = self._required_size()
            term = shutil.get_terminal_size(fallback=(80, 24))
            if term.columns < req_cols:
                msg = (
                    "Terminal is too narrow: "
                    f"{req_cols} cols are needed for rendering, "
                    f"current width is {term.columns} cols. "
                    "Resize and try again."
                )
                sys.stdout.write(msg + "\n")
                sys.stdout.flush()
                return

        revealed: set[Tuple[int, int]] = set()
        for coord in self.path:
            revealed.add(coord)
            frame_lines = self._build_static_lines(reveal_path=revealed)
            frame_text = "\n".join(frame_lines)
            # Clear screen and print frame
            sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
            sys.stdout.flush()
            sys.stdout.write(frame_text + "\n")
            sys.stdout.flush()
            time.sleep(0.05)

        return
