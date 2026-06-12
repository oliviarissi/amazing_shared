
import pytest

from maze.graph import Graph
from maze.structs import Wall, Cell, MazeSpecs

@pytest.fixture
def test_maze():
    maze_dict = {"WIDTH": "10",
            "HEIGHT": "10",
            "ENTRY": "2,9",
            "EXIT": "5,5",
            "OUTPUT_FILE": "out.txt",
            "PERFECT": True}

    return MazeSpecs(**maze_dict)


def test_blueprint(test_maze):
    with pytest.raises(Exception, match="too small"):
        Graph(test_maze)

