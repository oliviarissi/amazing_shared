


def hex_exporter(self, c_items: list[C], w_items: list[W]) -> dict:
    """
    Function takes list of cells, and walls.
    Input walls are result of generator - closed walls in maze.
    """
    
    c_bits: dict[C, int] = {c: 0 for c in c_items}

    directions_dict = {(d.value[0], d.value[1]): d for d in Directions}

    for item in w_items:
        dx = item.b.x - item.a.x
        dy = item.b.y - item.a.y
        a_direction = directions_dict[(dx, dy)]
        b_direction = directions_dict[(-dx, -dy)]
        c_bits[item.a] |= (1 << a_direction.value[2])
        c_bits[item.b] |= (1 << b_direction.value[2])

    return c_bits