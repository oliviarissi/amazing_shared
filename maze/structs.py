
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class MazeSpecs(BaseModel, extra='allow'):
    width: int = Field(ge=2, validation_alias='WIDTH')
    height: int = Field(ge=2, validation_alias='HEIGHT')
    entry_point: tuple[int, int] = Field(validation_alias='ENTRY')
    exit_point: tuple[int, int] = Field(validation_alias='EXIT')
    output_name: str = Field(min_length=4, pattern=r".*\.txt$",
                             validation_alias='OUTPUT_FILE')
    perfect: bool = Field(default=False, validation_alias='PERFECT')
    seed: int | None = Field(default=None, ge=1, validation_alias='SEED')

    @field_validator('entry_point', 'exit_point', mode='before')
    @classmethod
    def int_tuple(cls, data: str) -> tuple[int, int]:
        x, y = data.split(',', 1)
        if int(x) < 0 or int(y) < 0:
            raise ValueError("Coordinates must be positive")
        else:
            return (int(x), int(y))

    @model_validator(mode='after')
    def check_exit_entry(self) -> 'MazeSpecs':
        if self.entry_point == self.exit_point:
            raise ValueError("Entry and Exit point must be different.")

        ex, ey = self.entry_point
        if ex >= self.width or ey >= self.height:
            raise ValueError(f"Entry point {self.entry_point} "
                             f"outside maze bounds.")

        ex, ey = self.exit_point
        if ex >= self.width or ey >= self.height:
            raise ValueError(f"Exit point {self.exit_point} "
                             f"outside maze bounds.")

        return self


class Directions(Enum):
    """Each direction stores dx, dy, and bit."""
    NORTH = (0, -1, 0)
    EAST = (1, 0, 1)
    SOUTH = (0, 1, 2)
    WEST = (-1, 0, 3)


@dataclass(frozen=True)
class Cell:
    """each cell is a dsu component"""
    x: int
    y: int
    is_active: bool = field(default=True, compare=False, hash=False)


@dataclass(frozen=True)
class Wall:
    """remembers which 2 cells it connects"""
    cell_a: Cell = field(compare=True)
    cell_b: Cell = field(compare=True)
    is_boundary: bool = field(default=False, compare=False)

    # def __post_init__(self) -> None:
    #     # Check if they need to be swapped
    #     if (self.cell_b.x, self.cell_b.y) < (self.cell_a.x, self.cell_a.y):
    #         # Bypass frozen restriction to sort them in-place
    #         object.__setattr__(self, 'cell_a', self.cell_b)
    #         object.__setattr__(self, 'cell_b', self.cell_a)
    def __post_init__(self) -> None:
        # Check if they need to be swapped
        if (self.cell_b.x, self.cell_b.y) < (self.cell_a.x, self.cell_a.y):
            # Store the original cell_a safely
            temp_a = self.cell_a

            # Bypass frozen restriction to sort them in-place
            object.__setattr__(self, 'cell_a', self.cell_b)
            object.__setattr__(self, 'cell_b', temp_a)
