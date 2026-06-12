
# RESET = "\033[0m"
# RED = "\033[31m"
# GREEN = "\033[32m"
# BLUE = "\033[34m"
# CYAN = "\033[36m"
# YELLOW = "\033[33m"
# WHITE = "\033[37m"

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    RESET: str
    WALL: str
    ENTRY: str
    EXIT: str
    PATH: str
    EMPTY: str
    INACTIVE: str


DEFAULT_THEME = Theme(
    RESET="\033[0m",
    WALL="\033[37m",   # white
    ENTRY="\033[32m",  # green
    EXIT="\033[31m",   # red
    PATH="\033[36m",   # cyan
    EMPTY=" ",
    INACTIVE="\033[32m",
)

NEON_THEME = Theme(
    RESET="\033[0m",
    WALL="\033[35m",   # magenta
    ENTRY="\033[92m",  # bright green
    EXIT="\033[91m",   # bright red
    PATH="\033[96m",   # bright cyan
    EMPTY="·",
    INACTIVE="\033[32m",
)

DARK_THEME = Theme(
    RESET="\033[0m",
    WALL="\033[90m",   # dark gray
    ENTRY="\033[32m",  # green
    EXIT="\033[31m",   # red
    PATH="\033[34m",   # blue
    EMPTY=" ",
    INACTIVE="\033[32m",
)
