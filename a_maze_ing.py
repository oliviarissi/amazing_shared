
import sys
from src.graph import Graph
from src.parser import ConfigParser
from maze.generator import KruskalGenerator, WilsonGenerator
from maze.exporter import Exporter
from maze.bfs import BFS
from ui import run_ui


def main():  # Include try and except block
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        parser = ConfigParser()
        input_config = parser.read_txt(file_name)
        maze_specs = parser.validate_config(input_config)  # Error Raised if failed
        graph = Graph(maze_specs)

        if maze_specs.perfect:
            generator = KruskalGenerator()
        else:
            generator = WilsonGenerator()

        if graph.go_visual:
            run_ui(maze_specs, graph, generator)
        else:
            entry = maze_specs.entry_point
            exit_ = maze_specs.exit_point

            maze_raw = generator.generate(graph)  # TAKE LIST OF STR FROM EXPORTER
            solver = BFS(graph, maze_raw)  # get a class
            path_raw = solver.solve_maze(entry, exit_)

            exporter = Exporter(graph, maze_raw, path_raw, maze_specs)
            exporter.write_to_file()
            print("Graph too small for 42 pattern. Please adjust size")


if __name__ == "__main__":
    main()
