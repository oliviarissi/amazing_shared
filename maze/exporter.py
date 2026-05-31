from typing import TypeVar
C = TypeVar("C")  #added
from maze.structs import Directions
from src.graph import Graph  #added 
from maze.structs import Wall, Cell, MazeSpecs  #added


class Exporter:

    def __init__(self, graph: Graph, maze: list[Wall], solution: list[Cell], specs: MazeSpecs) -> None:
        self._dir_dict: dict[tuple, str] = {(d.value[0], d.value[1]): d for d in Directions}
        self.all_cells: list[Cell] = graph.cells
        self.maze_walls: list[Wall] = maze
        self.solution_path = solution
        self.ent: tuple[int, int] = specs.entry_point  #split in 2 lines
        self.ext: tuple[int, int] = specs.exit_point  #split in 2 lines
        self.output_file: str = specs.output_name
        

    def _build_bitmask(self) -> dict[C, int]:
        # separate the concerns
        # compute bitmasks
        c_bits: dict[C, int] = {c: 0 for c in self.all_cells}  #self.all_cells replace c_items

        for wall in self.maze_walls:
            dx = wall.cell_b.x - wall.cell_a.x  # dx = wall.b.x - wall.a.x
            dy = wall.cell_b.y - wall.cell_a.y  # dy = wall.b.y - wall.a.y
            a_direction = self._dir_dict[(dx, dy)]
            b_direction = self._dir_dict[(-dx, -dy)]
            c_bits[wall.cell_a] |= (1 << a_direction.value[2])  # c_bits[wall.a] |= (1 << a_direction.value[2])
            c_bits[wall.cell_b] |= (1 << b_direction.value[2])  # c_bits[wall.b] |= (1 << b_direction.value[2])

        return c_bits

    def _build_path_str(self) -> list[str]:
        # compute path str from list
        path_str: list[str] = []
        for c_a, c_b in zip(self.solution_path, self.solution_path[1:]):
            dx = c_b.x - c_a.x
            dy = c_b.y - c_a.y
            path_dir = self._dir_dict[(dx, dy)]
            path_str.append(path_dir.name[0])
        return path_str

    def _build_grid(self) -> list[str]:
        # build list of output str from bitmask
        bitmask: dict[C, int] = self._build_bitmask()
        lookup_dict: dict[tuple, int] = {(c.x, c.y): bits for c, bits in bitmask.items()}
        max_x: int = max(c.x for c in bitmask)  # bitmask replace c_bits
        max_y: int = max(c.y for c in bitmask)  # bitmask replace c_bits

        string_lst: list[str] = []
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                string_lst.append(format(lookup_dict[(x,y)], 'x'))
        return string_lst

    def write_to_file(self) -> None:
        # writes to output file
        grid_str: list[str] = self._build_grid()
        path_str: str = ''.join(self._build_path_str()) # path_str: str = self._build_path_str()
        entry: str = ','.join(map(str, self.ent))  # entry: str = ','.join(self.ent)
        extry: str = ','.join(map(str, self.ext))  # extry: str = ','.join(self.ext)
        print(len(self.solution_path)) #added
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:  # with open(self.output_file) as f:
                f.write('\n'.join(grid_str))
                f.write('\n')
                f.write('\n'.join([entry, extry]))
                f.write('\n')
                f.write(path_str)
                f.write('\n')
        except (FileExistsError, Exception) as e:  #brackets added
            print(f"Error writing to output - {e}")




            