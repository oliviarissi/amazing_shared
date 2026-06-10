import os

from renderer import MazeRenderer
from themes import DEFAULT_THEME, NEON_THEME, DARK_THEME

from maze.structs import MazeSpecs
from parser import parse_maze_file
from path_convertor import path_to_coords

from src.graph import Graph
from maze.generator import MazeGenerator
from maze.exporter import Exporter
from maze.bfs import BFS

# Maze builder import

def clear_screen() -> None:
    """Clear terminal screen."""
    os.system("cls" if os.name == "nt" else "clear")


def run_ui(specs: MazeSpecs, graph: Graph, generator: MazeGenerator) -> None:
    """Run terminal UI."""

    # data: dict = parse_maze_file("maze_example_subject.txt")
    # path = path_to_coords(entry, "EENNNEESSWWNNEEENESWNNEE")

    entry = specs.entry_point
    exit_= specs.exit_point

    maze_raw = generator.generate(graph) # TAKE LIST OF SRTING STOM EXPORTER
    solver = BFS(graph, maze_raw) #get a class
    path_raw = solver.solve_maze(entry, exit_)
    
    exporter = Exporter(graph, maze_raw, path_raw, specs)
    exporter.write_to_file()

    maze = exporter.maze_grid
    path_raw = exporter.path_str
    path = path_to_coords(entry, path_raw) # Isnt this useless, take path in different format
    # take path raw and make a look up dict

    cells = graph.cells.copy()

    show_path = True
    theme = DEFAULT_THEME

    while True:

        clear_screen()

        renderer = MazeRenderer(
            maze=maze,
            cells=cells,
            entry=entry,
            exit_=exit_,
            path=path if show_path else None,
            theme=theme,
        )

        renderer.render()

        print("\nCommands:")
        print("[p] Toggle path")
        print("[r] Regenerate maze")
        print("[t] switch theme")
        print("[q] Quit")
        
        command = input("\n> ").strip().lower()

        if command == "q":
            break
        
        elif command == "p":
            show_path = not show_path

        elif command == "r":
            if specs.seed:
                show_path = True
            else:
                # maze = run generator
                # path = run path solver
                #show_path = True
                show_path = True
                
        
        elif command == "t":
            if theme == DEFAULT_THEME:
                theme = NEON_THEME
            elif theme == NEON_THEME:
                theme = DARK_THEME
            else:
                theme = DEFAULT_THEME