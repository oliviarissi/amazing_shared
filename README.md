*This project has been created as part of the 42 curriculum by mmirdama, brisnovs*

# A-Maze-ing

A sophisticated maze generator and solver that creates and navigates mazes using advanced graph algorithms. This project implements multiple maze generation algorithms and provides a modular, reusable architecture for maze-related operations.

## Description

A-Maze-ing is a Python-based maze generation and solving framework. It generates perfect or imperfect mazes of arbitrary dimensions and automatically solves them using graph traversal algorithms. The project demonstrates clean architecture principles with separation of concerns across multiple modules.

### Key Features

- **Multiple Generation Algorithms**: Choose between Kruskal's algorithm (for perfect mazes) or Wilson's algorithm (for varied maze characteristics)
- **Maze Solving**: Uses Breadth-First Search (BFS) to find the shortest path from entry to exit
- **Configurable Specifications**: Easy configuration via text files with validation using Pydantic
- **Graph-Based Representation**: Represents mazes as graphs with cells and walls
- **Easter Egg**: Embeds the number "42" in the center of larger mazes as a fun detail
- **Automated Output**: Exports solved mazes to text files with visual representation

## Project Structure

```
A-Maze-ing/
├── a_maze_ing.py          # Entry point and main orchestration
├── sample_config.txt      # Example configuration file
├── requirements.txt       # Python dependencies
├── Makefile              # Build and run automation
├── src/                  # Core utilities
│   ├── graph.py          # Graph representation of the maze
│   ├── parser.py         # Configuration file parsing and validation
│   └── __init__.py
├── maze/                 # Maze-specific algorithms and utilities
│   ├── generator.py      # Maze generation algorithms
│   ├── bfs.py           # Pathfinding algorithm
│   ├── exporter.py      # Export maze to file
│   ├── structs.py       # Data structures (Cell, Wall, MazeSpecs)
│   ├── dsu.py           # Disjoint Set Union (Union-Find) data structure
│   └── __init__.py
└── tests/               # Test directory (for future test cases)
```

## Description of Algorithms

### Kruskal's Algorithm (Perfect Mazes)

Used when `PERFECT=True` in the configuration. This algorithm generates a "perfect maze" where there is exactly one path between any two cells.

**How it works:**
1. Start with all walls intact between cells
2. Randomly shuffle all walls
3. For each wall, check if the two cells it connects are in different sets (using DSU)
4. If they are in different sets, remove the wall and union the sets
5. Continue until all cells are connected
6. The remaining walls form the maze structure

**Characteristics:**
- Generates perfect mazes (no loops, single solution path)
- Uses the Disjoint Set Union (DSU/Union-Find) data structure for efficient connectivity checks
- Deterministic given the same random seed

### Wilson's Algorithm (Imperfect Mazes)

Used when `PERFECT=False` in the configuration. This algorithm generates mazes with multiple paths and loops.

**How it works:**
1. Start with a random seed cell marked as visited
2. While not all cells are visited:
   - Pick a random unvisited cell
   - Perform a random walk from that cell until hitting a visited cell
   - Erase any loops in the walk path
   - Add the walk path to the maze and mark all cells as visited
3. Remove walls along the connections made by the walk

**Characteristics:**
- Generates mazes with varied characteristics
- Can create imperfect mazes with multiple solutions
- Produces mazes with different visual properties than Kruskal's

### Breadth-First Search (BFS) - Maze Solving

Finds the shortest path from entry to exit in the solved maze.

**How it works:**
1. Build an adjacency map from the maze walls (only open passages)
2. Initialize a queue with the entry point
3. Perform BFS traversal, tracking visited cells and the path taken
4. When the exit is reached, backtrack through the "came_from" dictionary to reconstruct the path
5. Return the solution as an ordered list of cells

**Characteristics:**
- Guarantees the shortest path
- Time complexity: O(V + E) where V is cells and E is wall connections
- Simple and efficient for maze solving

## Configuration File Structure

The `sample_config.txt` file defines maze specifications using a simple `KEY=VALUE` format.

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `WIDTH` | Integer | Width of the maze (≥ 2) | `10` |
| `HEIGHT` | Integer | Height of the maze (≥ 2) | `10` |
| `ENTRY` | Tuple(int, int) | Starting coordinates `x,y` | `1,3` |
| `EXIT` | Tuple(int, int) | Ending coordinates `x,y` | `9,8` |
| `OUTPUT_FILE` | String | Output filename (must end in `.txt`) | `maze.txt` |
| `PERFECT` | Boolean | Generate perfect maze if `True` | `False` |

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `SEED` | Integer | Random seed for reproducibility (≥ 1) | `42` |

### Example Configuration

```
# Sample configuration for a 10x10 maze
WIDTH=10
HEIGHT=10
ENTRY=1,3
EXIT=9,8
OUTPUT_FILE=maze.txt
PERFECT=False
```

### Validation Rules

- Comments start with `#` and are ignored
- Empty lines are ignored
- Missing required keys raise a `ConfigError`
- Invalid values are caught by Pydantic validators:
  - Width and height must be ≥ 2
  - Entry and exit coordinates must be non-negative and within maze bounds
  - Entry and exit must be different points
  - Output filename must end with `.txt`

## Modularity and Reusability

The project is designed with modularity as a core principle. Each component is independent and can be reused in different contexts.

### Reusable Components

#### 1. **Graph Module** (`src/graph.py`)

**What it does:** Represents a maze as a graph of cells and walls.

**Reusable for:**
- Any grid-based pathfinding problem (tile-based games, robotics)
- Building adjacency structures for graph algorithms
- Creating visual representations of grid spaces

**How to reuse:**
```python
from src.graph import Graph
from maze.structs import MazeSpecs

specs = MazeSpecs(width=20, height=20, entry_point=(0, 0), 
                   exit_point=(19, 19), output_name="test.txt")
graph = Graph(specs)
# Now you have a graph with cells and walls for other algorithms
```

#### 2. **Parser Module** (`src/parser.py`)

**What it does:** Parses and validates configuration files using Pydantic.

**Reusable for:**
- Parsing any `KEY=VALUE` configuration files
- Other projects needing robust config validation with error messages
- Building configuration systems with type safety

**How to reuse:**
```python
from src.parser import ConfigParser

parser = ConfigParser()
config = parser.read_txt("config.txt")
validated_config = parser.validate_config(config)
# Works with any KEY=VALUE configuration format
```

#### 3. **Generator Algorithms** (`maze/generator.py`)

**What it does:** Abstract base class with two concrete maze generation implementations.

**Reusable for:**
- Implementing other maze generation algorithms (Prim's, Recursive Backtracking, etc.)
- Grid-based level generation in games
- Procedural dungeon generation

**How to reuse:**
```python
from maze.generator import MazeGenerator, KruskalGenerator
from src.graph import Graph

class MyCustomGenerator(MazeGenerator):
    def generate(self, graph: Graph):
        # Implement your algorithm here
        return your_maze_walls

# Drop-in replacement for KruskalGenerator or WilsonGenerator
generator = MyCustomGenerator()
maze = generator.generate(graph)
```

#### 4. **BFS Solver** (`maze/bfs.py`)

**What it does:** Finds shortest paths in maze graphs.

**Reusable for:**
- Any graph pathfinding problem
- Game AI pathfinding
- Network routing
- Robot navigation

**How to reuse:**
```python
from maze.bfs import BFS
from src.graph import Graph

solver = BFS(graph, maze_walls)
path = solver.solve_maze(start_point, end_point)
# Works on any connected graph with adjacency information
```

#### 5. **Data Structures** (`maze/structs.py`)

**What it does:** Pydantic models and dataclasses for type-safe data.

**Reusable for:**
- Creating validated data structures for other projects
- Building configuration systems with Pydantic
- Ensuring data integrity through validation

**How to reuse:**
```python
from maze.structs import Cell, Wall, MazeSpecs

# Use in your own projects for type safety
cell = Cell(x=5, y=10)
wall = Wall(cell_a=cell1, cell_b=cell2)
```

#### 6. **DSU Module** (`maze/dsu.py`)

**What it does:** Implements Union-Find data structure for efficient connectivity checking.

**Reusable for:**
- Detecting cycles in graphs
- Network connectivity problems
- Kruskal's algorithm for MST
- Any problem requiring efficient set operations

**How to reuse:**
```python
from maze.dsu import DSU

cells = [...]
dsu = DSU(cells)
if not dsu.connected(cell_a, cell_b):
    dsu.union(dsu.find(cell_a), dsu.find(cell_b))
```

### Design Patterns Used

- **Abstract Base Class Pattern**: `MazeGenerator` allows extending with new algorithms
- **Strategy Pattern**: Different maze generation algorithms as interchangeable strategies
- **Validation with Pydantic**: Type-safe configuration handling
- **Separation of Concerns**: Parser, graph, generators, and solvers are independent

## Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/MoujanM/A-Maze-ing.git
cd A-Maze-ing
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or use the Makefile:
```bash
make all
```

### Running the Program

**Basic usage with default configuration:**
```bash
python a_maze_ing.py sample_config.txt
```

**Using the Makefile:**
```bash
make run
```

**Using the Makefile with custom configuration:**
```bash
make run CONFIG=your_config.txt
```

**Manual setup (if not using Makefile):**
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt
python a_maze_ing.py sample_config.txt
```

### Expected Output

The program generates a maze and saves it to the specified `OUTPUT_FILE` in the configuration. The output contains:
- Visual representation of the maze with walls
- Marked entry and exit points
- Solution path highlighted (typically with a different character)

### Creating Your Own Configuration

1. Copy `sample_config.txt` and modify the values:
```bash
cp sample_config.txt my_maze.txt
```

2. Edit the file with your desired parameters:
```
WIDTH=20
HEIGHT=20
ENTRY=2,2
EXIT=18,18
OUTPUT_FILE=my_maze.txt
PERFECT=True
```

3. Run the program:
```bash
python a_maze_ing.py my_maze.txt
```

### Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` | Ensure the config file exists in the current directory |
| `Validation failed` | Check config values match the required types and ranges |
| `Entry/Exit point not found` | Verify entry/exit coordinates are within maze bounds |
| Missing dependencies | Run `pip install -r requirements.txt` |

## Resources

### Dependencies

- **pydantic**: Data validation using Python type hints
- **numpy**: Numerical operations for maze grid representation
- **Typing**: Type hints for Python (stdlib in Python 3.5+)

### Useful References

#### Maze Generation Algorithms
- [Kruskal's Algorithm](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Wilson's Algorithm](https://en.wikipedia.org/wiki/Loop-erased_random_walk)
- [Maze Generation Algorithms Comparison](http://www.amazeinc.com/mazes.html)

#### Graph Theory
- [Breadth-First Search (BFS)](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Disjoint Set Union](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
- [Graph Representation](https://en.wikipedia.org/wiki/Graph_(discrete_mathematics))

### Learning Resources

- Interactive maze algorithm visualizations: [Maze Generation Visualizer](https://www.netsecstudent.com/2021/08/maze-generator.html)
- Algorithm tutorials: [Computerphile - Maze Generation](https://www.youtube.com/watch?v=HyK_Q5rrcr4)
- Graph theory course: [Khan Academy - Graph Algorithms](https://www.khanacademy.org/computing/computer-science/algorithms)


