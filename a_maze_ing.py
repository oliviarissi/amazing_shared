
import sys
from maze.graph import Graph
from src.parser import ConfigParser
from maze.generator import KruskalGenerator, WilsonGenerator, MazeGenerator
from src.exporter import Exporter
from maze.bfs import BFS
from src.ui import run_ui


def main() -> None:
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        try:
            parser = ConfigParser()
            input_config = parser.read_txt(file_name)
            maze_specs = parser.validate_config(input_config)
            graph = Graph(maze_specs)
            generator: MazeGenerator = WilsonGenerator()
            if maze_specs.perfect:
                generator = KruskalGenerator()

            if graph._graph_mask.all():
                print("Too small!")
                maze = generator.generate(graph)
                maze_solver = BFS(graph, maze)
                solution = maze_solver.solve_maze(maze_specs.entry_point,
                                                  maze_specs.exit_point)
                exporter = Exporter(graph.cell_lookup, maze,
                                    solution, maze_specs)
                exporter.write_to_file()

            else:
                run_ui(maze_specs, graph, generator)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
