from abc import ABC, abstractmethod
import random
from src.graph import Graph
from maze.structs import Wall, Directions, Cell  #added cell


class MazeGenerator(ABC):

    @abstractmethod
    def generate(self, graph: Graph) -> list[Wall]:
        # algorithm implementation goes here
        pass


class KruskalGenerator(MazeGenerator):

    def generate(self, graph: Graph) -> list[Wall]:
        from maze.dsu import DSU

        walls = graph.walls
        dsu = DSU(graph.cells)

        removed_walls: list[Wall] = []
        random.shuffle(walls)
        dsu_count = len(graph.cells)
        for wall in walls:
            if not dsu.connected(wall.cell_a, wall.cell_b):
                root_a = dsu.find(wall.cell_a)
                root_b = dsu.find(wall.cell_b)

                dsu.union(root_a, root_b)
                dsu_count -= 1
                removed_walls.append(wall)
            if dsu_count == 1:
                break
        
        for wall in removed_walls:
            walls.remove(wall)
        
        # if not perfect:
        #     extra = round(len(walls) * 0.05)
        #     random.shuffle(walls)
        #     for wall in walls[:extra]:
        #         walls.remove(wall)

        return walls


class WilsonGenerator(MazeGenerator):
    _DELTAS: list[tuple[int, int]] = [(d.value[0], d.value[1]) for d in Directions]

    def _random_walk(self, start: Cell, lookup_dict: dict[tuple[int, int], Cell],
                     visited: set[Cell]) -> list[Cell]:

        walk_path: list[Cell] = [start]
        seed: Cell = random.choice(lookup_dict.values())
        visited.add(seed)
        while start not in visited:
            dx, dy = random.choice(self._DELTAS)
            if (start.x + dx, start.y + dy) not in lookup_dict:
                continue
            neighbour = lookup_dict[start.x + dx, start.y + dy]
            walk_path = self._erase_loop(walk_path, neighbour)
            if neighbour in visited:
                break
            start = neighbour

        return walk_path

    def _erase_loop(self, path: list[Cell], new_cell: Cell) -> list[Cell]:

        if new_cell in path:
            loop_start = path.index(new_cell)
            del path[loop_start:]
        path.append(new_cell)
        
        return path

    def generate(self, graph: Graph) -> list[Wall]:

        all_cells: list[Cell] = graph.cells
        cell_lookup: dict[tuple[int, int], Cell] = {(c.x, c.y): c for c in all_cells}
        visited_cells: set[Cell] = set()
        walls_set: set[Wall] = set(graph.walls)
        
        while len(visited_cells) < len(all_cells):
            unvisited_cells: list[Cell] = [c for c in all_cells if c not in visited_cells]
            start: Cell = random.choice(unvisited_cells)

            walk_path = self._random_walk(start, cell_lookup, visited_cells)

            visited_cells.update(walk_path)
            
            for cell_a, cell_b in zip(walk_path, walk_path[1:]):
                connecting_wall = Wall(cell_a, cell_b)
                if connecting_wall in walls_set:
                    walls_set.remove(connecting_wall)

        return list(walls_set)



