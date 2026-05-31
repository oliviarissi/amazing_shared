
from maze.structs import Wall, Cell, MazeSpecs
import numpy as np

class Graph():
    """Given a height & width, get all possible walls and cells"""
    
    def __init__(self, specs: MazeSpecs):
        self.width: int = specs.width
        self.height: int = specs.height

        self.blueprint: np.ndarray = self.easter_egg()

        self.cells: list[Cell] = self._build_cells(self.blueprint)
        self.walls: list[Wall] = self._build_walls()

    def _build_cells(self, blueprint: np.ndarray) -> list[Cell]:
        cells = []
        for y in range(self.height):
            for x in range(self.width):
                # cell = Cell(x, y)

                #if blueprint[y, x] == False:
                    #cell.is_active = False
                
                #cells.append(cell)

                is_active = bool(blueprint[y, x])  # NEW
                cell = Cell(x, y, is_active=is_active)
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

        #for cell in self.cells:  
        #    for dx, dy in direction:
        #        nx, ny = cell.x + dx, cell.y + dy
        #        if self._inside_check(nx, ny):
        #            neighbour_cell = Cell(nx, ny)
        #            if cell.is_active and neighbour_cell.is_active:
        #                walls.append(Wall(cell, neighbour_cell))
        #return walls
    
        # map coordinates to the single Cell instances created above
        cell_map = {(c.x, c.y): c for c in self.cells}  # NEW
        for cell in self.cells:
            if not cell.is_active:
                continue
            for dx, dy in direction:
                nx, ny = cell.x + dx, cell.y + dy
                if self._inside_check(nx, ny):
                    neighbour_cell = cell_map[(nx, ny)]
                    if neighbour_cell.is_active:
                        walls.append(Wall(cell, neighbour_cell))
        return walls

    def easter_egg(self) -> np.ndarray:
        """
        Hard-coded grid masking of 42.
        to be placed in centre of graph if size allows.
        """
        graph_mask = np.ones((self.height, self.width), dtype=bool)

        four = np.zeros((5, 3), dtype=int)
        four[0:2, 0] = 1
        four[2, :] = 1
        four[0:2, 2] = 1
        two = np.zeros((5,3), dtype=int)
        two[[0, 2, 4], :] = 1
        two[1, 2] = 1
        two[3, 0] = 1
        spacer = np.zeros((5, 1), dtype=int)
        stamp_42 = np.hstack([four, spacer, two])

        stamp_h = stamp_42.shape[0]
        stamp_w = stamp_42.shape[1]

        if self.height >= stamp_h * 2 + 2 and self.width >= stamp_w * 2 + 2:
            start_x = (self.width // 2) - ( stamp_w // 2)
            start_y = (self.height // 2) - (stamp_h // 2)

            graph_mask[start_y : start_y + stamp_h, start_x : start_x + stamp_w] = (stamp_42 == 0)
        else:
            raise Exception("Graph too small for the central stamp!")

        return graph_mask




            






        