from typing import List, Tuple

def path_to_coords(
    start: Tuple[int, int],
    path: str,
) -> List[Tuple[int, int]]:
    """
     Convert movement string (N/E/S/W) into an ordered list of coordinates.

    Args:
        start: starting position (x, y)
        path: string like "EESWN"

    Returns:
        set of visited coordinates
    """

    x, y = start
    coords: List[Tuple[int, int]] = [(x, y)]

    moves = {
        "N": (0, -1),
        "S": (0, 1),
        "E": (1, 0),
        "W": (-1, 0),
    }

    for step in path:
        if step not in moves:
            continue  # raise error !

        dx, dy = moves[step]
        x += dx
        y += dy
        coords.append((x, y))

        # if x < 0 or y < 0 or x >= width or y >= height: raise ValueError("Path goes outside maze")

    return coords