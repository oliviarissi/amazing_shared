from abc import ABC, abstractmethod
import random
from graph import Graph
from structs import Wall, Cell
from bfs import BFS


class MazeGenerator(ABC):

    @abstractmethod
    def generate(self, graph: Graph) -> list[Wall]:
        # algorithm implementation goes here
        pass

    def solve_maze(self, graph: Graph, maze: list[Wall]) -> list[Cell]:
        solver: BFS = BFS(graph, maze)

        return solver.solve_maze()


class KruskalGenerator(MazeGenerator):

    def generate(self, graph: Graph) -> list[Wall]:
        from dsu import DSU

        maze_walls: list[Wall] = graph.walls.copy()
        active_cells: list[Cell] = [c for c in graph.cells if c.is_active]
        dsu = DSU(active_cells)

        removable_walls: list[Wall] = [w for w in maze_walls
                                       if w.cell_a.is_active and
                                       w.cell_b.is_active]

        removed_walls: list[Wall] = []
        random.shuffle(removable_walls)

        for wall in removable_walls:
            if not dsu.connected(wall.cell_a, wall.cell_b):
                root_a = dsu.find(wall.cell_a)
                root_b = dsu.find(wall.cell_b)

                dsu.union(root_a, root_b)
                removed_walls.append(wall)

        for wall in removed_walls:
            maze_walls.remove(wall)

        return maze_walls


class WilsonGenerator(MazeGenerator):

    def _random_walk(self, start: Cell,
                     lookup_dict: dict[tuple[int, int], Cell],
                     visited: set[Cell]) -> list[Cell]:
        walk_path: list[Cell] = [start]
        direction: list[tuple[int, int]] = [(1, 0), (0, 1)]

        while start not in visited:
            valid_neighbours: list[Cell] = []
            for dx, dy in direction:
                if (start.x + dx, start.y + dy) in lookup_dict:
                    valid_neighbours.append(lookup_dict[start.x + dx,
                                                        start.y + dy])
            if not valid_neighbours:
                break
            neighbour = random.choice(valid_neighbours)
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

        lookup_dict: dict[tuple[int, int], Cell] = graph.cell_lookup
        active_cells: list[Cell] = [c for c in graph.cell_lookup.values()
                                    if c.is_active]
        visited_cells: set[Cell] = set()
        walls_set: set[Wall] = set(graph.walls.copy())
        seed: Cell = random.choice(active_cells)
        visited_cells.add(seed)

        while len(visited_cells) < len(active_cells):
            unvisited_cells: list[Cell] = ([c for c in active_cells
                                            if c not in visited_cells])
            start: Cell = random.choice(unvisited_cells)

            walk_path = self._random_walk(start, lookup_dict,
                                          visited_cells)

            visited_cells.update(walk_path)

            for cell_a, cell_b in zip(walk_path, walk_path[1:]):
                connecting_wall = Wall(cell_a, cell_b)
                if connecting_wall in walls_set:
                    walls_set.remove(connecting_wall)

        return list(walls_set)
