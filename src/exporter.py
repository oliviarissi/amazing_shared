
from maze.structs import Directions, Cell, Wall, MazeSpecs
from typing import Iterator


class Exporter:
    _DIR_DICT: dict[tuple[int, int], Directions] = ({
        (d.value[0], d.value[1]): d for d in Directions})

    def __init__(self, cell_lookup: dict[tuple[int, int], Cell],
                 maze: list[Wall], solution: list[Cell],
                 specs: MazeSpecs) -> None:

        self._cell_lookup = cell_lookup
        self.all_cells: list[Cell] = list(self._cell_lookup.values())

        self.maze_walls: list[Wall] = maze
        self.solution_path: list[Cell] = solution
        self.entry_point: tuple[int, int] = specs.entry_point
        self.exit_point: tuple[int, int] = specs.exit_point
        self.output_file: str = specs.output_name

        self._bitmask: dict[Cell, int] = self._build_bitmask()
        self._maze_grid: list[list[int]] = self._build_grid_matrix()

        self.path_str: str = self._build_path_str()

    def _build_bitmask(self) -> dict[Cell, int]:

        c_bits: dict[Cell, int] = {c: (0 if c.is_active else 0xF)
                                   for c in self.all_cells}
        active_cells: list[Cell] = [c for c in self.all_cells if c.is_active]
        for wall in self.maze_walls:
            dx = wall.cell_b.x - wall.cell_a.x
            dy = wall.cell_b.y - wall.cell_a.y
            a_direction = self._DIR_DICT[(dx, dy)]
            b_direction = self._DIR_DICT[(-dx, -dy)]
            if wall.cell_a.is_active:
                c_bits[wall.cell_a] |= (1 << a_direction.value[2])
            if wall.cell_b.is_active:
                c_bits[wall.cell_b] |= (1 << b_direction.value[2])

        for cell in active_cells:
            for direction in Directions:
                dx, dy, bit = direction.value
                neighbour = self._cell_lookup.get((cell.x + dx, cell.y + dy))
                if neighbour is None:
                    c_bits[cell] |= (1 << bit)

        return c_bits

    def _build_grid_matrix(self) -> list[list[int]]:
        lookup = {(c.x, c.y): bit for c, bit in self._bitmask.items()}
        max_x = max(x for x, y in lookup)
        max_y = max(y for x, y in lookup)
        grid = [
            [lookup[(x, y)] for x in range(max_x + 1)]
            for y in range(max_y + 1)
        ]

        return grid

    def _grid_rows(self) -> Iterator[str]:
        """Yield hex rows (strings) from the precomputed matrix."""
        for row in self._maze_grid:
            yield ''.join(format(v, 'x') for v in row)

    def _build_path_str(self) -> str:
        # compute path str from list
        path_str: list[str] = []
        for c_a, c_b in zip(self.solution_path, self.solution_path[1:]):
            dx = c_b.x - c_a.x
            dy = c_b.y - c_a.y
            path_dir = self._DIR_DICT[(dx, dy)]
            path_str.append(path_dir.name[0])
        return ''.join(path_str)

    def write_to_file(self) -> None:
        # writes to output file
        entry_str: str = ','.join([str(self.entry_point[0]),
                                   str(self.entry_point[1])])
        extit_str: str = ','.join([str(self.exit_point[0]),
                                   str(self.exit_point[1])])
        try:
            with open(self.output_file, mode='w') as f:
                for row in self._grid_rows():
                    f.write(row + '\n')
                f.write('\n\n')
                f.write('\n'.join([entry_str, extit_str]))
                f.write('\n')
                f.write(self.path_str)
                f.write('\n')
        except Exception as e:
            print(f"Error writing to output - {e}")
