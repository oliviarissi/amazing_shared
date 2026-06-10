
from maze.structs import Directions, Cell, Wall, MazeSpecs
from src.graph import Graph


class Exporter:

    def __init__(self, graph: Graph, maze: list[Wall],
                 solution: list[Cell], specs: MazeSpecs) -> None:
        self._dir_dict: dict[tuple[int, int], Directions] = (
            {(d.value[0],
             d.value[1]): d for d in Directions}
        )
        self.all_cells: list[Cell] = graph.cells
        self.maze_walls: list[Wall] = maze
        self.solution_path: list[Cell] = solution
        self.entry_point: tuple[int, int] = specs.entry_point
        self.exit_point: tuple[int, int] = specs.exit_point
        self.output_file: str = specs.output_name
        self.path_str: str = self._build_path_str()
        self.maze_hex: str = self._build_grid()
        self.maze_grid: list[list[int]] = self._build_grid_matrix()

    def _build_grid_matrix(self) -> list[list[int]]:
        bitmask = self._build_bitmask()
        lookup = {(c.x, c.y): bit for c, bit in bitmask.items()}
        max_x = max(x for x, y in lookup)
        max_y = max(y for x, y in lookup)
        grid = [[lookup[(x, y)] for x in range(max_x+1)] for y in range(max_y+1)]

        return grid

    def _build_bitmask(self) -> dict[Cell, int]:
        # separate the concerns
        # compute bitmasks
        c_bits: dict[Cell, int] = {c: 0 for c in self.all_cells}

        for wall in self.maze_walls:
            dx = wall.cell_b.x - wall.cell_a.x
            dy = wall.cell_b.y - wall.cell_a.y
            a_direction = self._dir_dict[(dx, dy)]
            b_direction = self._dir_dict[(-dx, -dy)]
            c_bits[wall.cell_a] |= (1 << a_direction.value[2])
            c_bits[wall.cell_b] |= (1 << b_direction.value[2])

        return c_bits

    def _build_path_str(self) -> list[str]:
        # compute path str from list
        path_str: list[str] = []
        for c_a, c_b in zip(self.solution_path, self.solution_path[1:]):
            dx = c_b.x - c_a.x
            dy = c_b.y - c_a.y
            path_dir = self._dir_dict[(dx, dy)]
            path_str.append(path_dir.name[0])
        path_single_str = ''.join(p for p in path_str)
        return path_single_str

    def _build_grid(self) -> list[str]:
        # build list of output str from bitmask
        bitmask: dict[Cell, int] = self._build_bitmask()
        lookup_dict: dict[tuple[int, int], int] = {(c.x, c.y): bit for c, bit in bitmask.items()}
        max_x: int = max(x for x, y in lookup_dict)
        max_y: int = max(y for x, y in lookup_dict)

        string_lst: list[str] = []
        for y in range(max_y + 1):
            row_str: str = ""
            for x in range(max_x + 1):
                row_str += format(lookup_dict[(x, y)], 'x')
                if x == max_x:
                    string_lst.append(row_str)

        maze_str = '\n'.join(string_lst)
        return maze_str

    def write_to_file(self) -> None:
        # writes to output file
        entry: str = ','.join([str(self.entry_point[0]),
                               str(self.entry_point[1])])
        extry: str = ','.join([str(self.exit_point[0]),
                               str(self.exit_point[1])])
        try:
            with open(self.output_file, mode='x') as f:
                f.write(self.maze_hex)
                f.write('\n\n')
                f.write('\n'.join([entry, extry]))
                f.write('\n')
                f.write(self.path_str)
                f.write('\n')
        except (FileExistsError, Exception) as e:
            print(f"Error writing to output - {e}")
