import time
import sys
import os
import shutil

from typing import List, Tuple, Optional, Set, Iterable
from themes import Theme, DEFAULT_THEME, NEON_THEME, DARK_THEME
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
        cells: list[Cell],
        entry: Tuple[int, int],
        exit_: Tuple[int, int],
        path: Optional[Iterable[Tuple[int, int]]] = None,
        theme: Theme = DEFAULT_THEME,
        frame_delay: float = 0.05,
        clear_before: bool = False,
    ) -> None:
        self.maze = maze
        self.cells = cells
        self.entry = entry
        self.exit = exit_
        self.path = path
        self.theme = theme
        self.frame_delay = frame_delay
        self.clear_before = clear_before

    def _build_static_lines(
            self, reveal_path: Optional[Set[Tuple[int, int]]] = None
    ) -> List[str]:
        if not self.maze or not self.maze[0]:
            return ["Empty maze"]

        height = len(self.maze)
        width = len(self.maze[0])
        output: list[str] = []

        cell_lookup = {(c.x, c.y): c for c in self.cells}

        top = f"{self.theme.WALL}+"
        for x in range(width):
            if self.maze[0][x] & NORTH:
                top += "   +"
            else:
                top += "---+"
        output.append(top)

        for y in range(height):
            middle = f"{self.theme.WALL}|"
            bottom = f"{self.theme.WALL}+"
            for x in range(width):
                cell = self.maze[y][x]

                cobj = cell_lookup.get((x, y))
                is_active = True if cobj is None else bool(cobj.is_active)

                if not is_active:
                    content = f"{self.theme.INACTIVE}X{self.theme.RESET}"
                else:
                    content = " "
                    if (x, y) == self.entry:
                        content = f"{self.theme.ENTRY}S{self.theme.RESET}"
                    elif (x, y) == self.exit:
                        content = f"{self.theme.EXIT}E{self.theme.RESET}"
                    elif reveal_path is not None and (x, y) in reveal_path:
                        content = f"{self.theme.PATH}X{self.theme.RESET}"

                if cell & EAST:
                    middle += f" {content} {self.theme.WALL}|{self.theme.RESET}"
                else:
                    if x == width - 1:
                        middle += f" {content} {self.theme.WALL}|{self.theme.RESET}"
                    else:
                        middle += f" {content}  "

                if cell & SOUTH:
                    bottom += "---+"
                else:
                    if y == height - 1:
                        bottom += "---+"
                    else:
                        bottom += "   +"

            output.append(middle)
            output.append(bottom)

        output.append(self.theme.RESET)
        return output

    def _required_size(self) -> Tuple[int, int]:
        """Return (cols, rows) required to render the maze fully."""
        height = len(self.maze)
        width = len(self.maze[0])
        cols = 0
        # top border: each cell contributes 4 chars plus final "+"
        cols = 1 + width * 4
        # each content line same width
        rows = 1 + height * 2  # top border + (middle+bottom) per row
        # +1 for trailing RESET line if any
        rows += 1
        return cols, rows

    def _supports_cursor(self) -> bool:
        return sys.stdout.isatty()

    def render(self) -> str:
        """Render maze. Print/animate frames to stdout;
        return final maze string."""
        if not self.maze or not self.maze[0]:
            out = "Empty maze"
            sys.stdout.write(out + "\n")
            sys.stdout.flush()
            return out

        # If path is None -> never reveal path; print static maze
        if self.path is None:
            final = "\n".join(self._build_static_lines(reveal_path=set()))
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return final

        # If path is a set -> static full path (print once)
        if isinstance(self.path, set):
            final = "\n".join(self._build_static_lines(reveal_path=self.path))
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return final

        # Try to coerce to sequence for animation
        try:
            seq = list(self.path)
        except Exception:
            final = "\n".join(self._build_static_lines(reveal_path=set()))
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return final

        # If terminal doesn't support cursor ops, fallback to static final path (print once)
        supports_cursor = self._supports_cursor()
        if not supports_cursor:
            final = "\n".join(self._build_static_lines(reveal_path=set(seq)))
            sys.stdout.write(final + "\n")
            sys.stdout.flush()
            return final

        # Check terminal size before drawing
        req_cols, req_rows = self._required_size()
        term = shutil.get_terminal_size(fallback=(80, 24))
        if term.columns < req_cols or term.lines < req_rows:
            msg = (
                f"Terminal too small: need {req_cols}×{req_rows}, "
                f"current {term.columns}×{term.lines}. Resize and try again."
            )
            sys.stdout.write(msg + "\n")
            sys.stdout.flush()
            # return msg

        # Optionally clear before drawing
        if self.clear_before:
            os.system("cls" if os.name == "nt" else "clear")

        revealed: set[Tuple[int, int]] = set()
        for coord in seq:
            revealed.add(coord)
            frame_lines = self._build_static_lines(reveal_path=revealed)
            frame_text = "\n".join(frame_lines)
            # Clear screen and print frame
            if supports_cursor:
                # ANSI clear+home is faster than external clear
                sys.stdout.write("\x1b[H\x1b[2J\x1b[3J")
                sys.stdout.flush()
            else:
                os.system("cls" if os.name == "nt" else "clear")
            sys.stdout.write(frame_text + "\n")
            sys.stdout.flush()
            time.sleep(self.frame_delay)

        final = "\n".join(self._build_static_lines(reveal_path=set(seq)))
        # ensure final is returned
        return final
