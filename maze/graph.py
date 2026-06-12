
from maze.structs import Wall, Cell, MazeSpecs
import numpy as np


class Graph():
    """Given a height & width, get all possible walls and cells"""

    def __init__(self, specs: MazeSpecs):
        self.width: int = specs.width
        self.height: int = specs.height
        self._graph_mask = self.easter_egg()
        # in ui we can check if all are active or not

        self.cells: list[Cell] = self._build_cells()
        self.cell_lookup: dict[tuple[int, int], Cell] = ({(c.x, c.y): c for
                                                          c in self.cells})
        self.walls: list[Wall] = self._build_walls()

    def _build_cells(self) -> list[Cell]:
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x, y, is_active=bool(self._graph_mask[y, x]))
                cells.append(cell)
        return cells

    def _inside_check(self, x: int, y: int) -> bool:
        # check to see if given coordinates within bounds of graph
        return 0 <= x < self.width and 0 <= y < self.height

    def _build_walls(self) -> list[Wall]:
        """
        Walls connect two cells together.
        func only checks two directions to avoid dups.
        """
        direction = [(1, 0), (0, 1)]
        walls = []

        for cell in self.cells:
            for dx, dy in direction:
                nx, ny = cell.x + dx, cell.y + dy
                if self._inside_check(nx, ny):
                    neighbour_cell = self.cell_lookup[(nx, ny)]
                    if cell.is_active or neighbour_cell.is_active:
                        boundary: bool = not (cell.is_active and
                                              neighbour_cell.is_active)
                        walls.append(Wall(cell, neighbour_cell,
                                          is_boundary=boundary))

        return walls

    def easter_egg(self) -> np.ndarray:
        """
        function returns a graph-mask; marking active/inactive cells.
        if the size allows, the graph-mask includes the central stamp.
        else it returns graph with all active cells.
        """

        graph_mask: np.ndarray = np.ones((self.height, self.width), dtype=bool)
        four = np.zeros((5, 3), dtype=int)
        four[0:2, 0] = 1
        four[2, :] = 1
        four[:, 2] = 1
        two = np.zeros((5, 3), dtype=int)
        two[[0, 2, 4], :] = 1
        two[1, 2] = 1
        two[3, 0] = 1
        spacer = np.zeros((5, 1), dtype=int)
        stamp_42 = np.hstack([four, spacer, two])

        stamp_h = stamp_42.shape[0]
        stamp_w = stamp_42.shape[1]

        if self.height >= stamp_h * 2 + 2 and self.width >= stamp_w * 2 + 2:
            start_x = (self.width // 2) - (stamp_w // 2)
            start_y = (self.height // 2) - (stamp_h // 2)

            graph_mask[start_y: start_y + stamp_h,
                       start_x: start_x + stamp_w] = (stamp_42 == 0)

        return graph_mask
