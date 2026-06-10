
import sys
import maze
from src.graph import Graph
from src.parser import ConfigParser
from maze.generator import KruskalGenerator, WilsonGenerator
from maze.exporter import Exporter
from maze.bfs import BFS
from ui import run_ui

def main():
    if len(sys.argv) == 2:  #added tab below
        file_name = sys.argv[1]
        parser = ConfigParser()  # had to create instance. Alternative we can have them as static methods
        input_config = parser.read_txt(file_name)
        maze_specs = parser.validate_config(input_config)  #Error Raised if failed
        graph = Graph(maze_specs)

        if maze_specs.perfect:
            generator = KruskalGenerator()  # Fixed typo
        else:
            generator = WilsonGenerator()  # Fixed typo

        if graph.go_visual:
            run_ui(maze_specs, graph, generator)
        else:
            entry = maze_specs.entry_point
            exit_= maze_specs.exit_point

            maze_raw = generator.generate(graph) # TAKE LIST OF SRTING STOM EXPORTER
            solver = BFS(graph, maze_raw) #get a class
            path_raw = solver.solve_maze(entry, exit_)
            
            exporter = Exporter(graph, maze_raw, path_raw, maze_specs)
            exporter.write_to_file()
            print("Graph too small for 42 pattern. Please adjust size")
        
        # maze = generator.generate(graph)
        # maze_solver = BFS(graph, maze)
        # solution = maze_solver.solve_maze(maze_specs.entry_point, maze_specs.exit_point)
        # exporter = Exporter(graph, maze, solution, maze_specs)
        # exporter.write_to_file()

    #print(maze_specs)
    # run_ui(maze_specs, graph)



if __name__ == "__main__":
    main()
    



    