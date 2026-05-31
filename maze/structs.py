
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, field_validator, model_validator
from enum import Enum


class MazeSpecs(BaseModel, extra='allow'):
    width: int = Field(ge=2, validation_alias='WIDTH')
    height: int = Field(ge=2, validation_alias='HEIGHT')
    entry_point: tuple[int, int] = Field(validation_alias='ENTRY')
    exit_point: tuple[int, int] = Field(validation_alias='EXIT')
    output_name: str = Field(min_length=4, pattern=".*\.txt$", validation_alias='OUTPUT_FILE')
    perfect: bool = Field(default=False, validation_alias='PERFECT')

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
        if ex > self.width or ey > self.height:
            raise ValueError(f"Entry point {self.entry_point} outside maze bounds.")
        
        ex, ey = self.exit_point
        if ex > self.width or ey > self.height:
            raise ValueError(f"Exit point {self.exit_point} outside maze bounds.")

        return self


class Directions(Enum):
    """Each direction stores dx, dy, and bit."""
    NORTH = (0, -1, 0)
    EAST = (1, 0, 2)
    SOUTH = (0, 1, 4)
    WEST = (-1, 0, 8)


@dataclass(frozen=True)
class Cell:
    """each cell is a dsu component"""
    x: int
    y: int
    is_active: bool = field(default=True)

@dataclass(frozen=True)
class Wall:
    """remembers which 2 cells it connects"""
    cell_a: Cell = field(compare=True)
    cell_b: Cell = field(compare=True)

# check the following again
# reasoning is Wall(cell_a, cell_b) == Wall(cell_b, cell_a)
    # @classmethod
    # def make(cls, a: Cell, b: Cell) -> cls:
    #     if (b.x, b.y) < (a.x, a.y):
    #         a, b = b, a
    #     return cls(a, b)




