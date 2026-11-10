"""
Lab 9
Arrrh
"""

def define_direction(previous_direction:str, azimuth:int) -> str:
    """
    Calculate the new path direction based on the current direction
    and the pirate's biased azimuth. The azimuth is given in degrees
    and can be any non-negative multiple of 90. The directions are 
    represented as 'N' for North, 'E' for East, 'S' for South, and 'W' 
    for West.

    Args:
    previous_direction (str): The current direction ('N', 'E', 'S', 'W').
    azimuth (int): The azimuth in degrees (non-negative multiple of 90).

    Returns:
    str: The new direction as a single character string.

    For example:
    - If the current direction is North ('N') and the azimuth is 90 degrees,
      the new direction will be East ('E').
    - If the current direction is South ('S') and the azimuth is 90 degrees,
      the new direction will be West ('W').

    >>> define_direction('N', 0)
    'N'
    >>> define_direction('N', 90)
    'E'
    >>> define_direction('N', 180)
    'S'
    >>> define_direction('N', 270)
    'W'
    >>> define_direction('E', 90)
    'S'
    >>> define_direction('W', 270)
    'S'
    """

    values = {'N': 0,
              'E': 90,
              'S': 180,
              'W': 270}

    true_direction = (values[previous_direction] + azimuth) % 360

    values_invert = {v: k for k, v in values.items()}

    return values_invert[true_direction]


def read_map(file_name: str) -> tuple[tuple, list]:
    """
    Reads a map from the specified file and interprets the directions
    and steps for navigation. The map file contains information about
    the starting coordinates and the steps to be taken in a specified
    direction. The initial direction is assumed to be North.

    The map file should be structured in such a way that it lists the
    starting coordinates (x, y) followed by directions (N, E, S, W)
    and the corresponding number of steps to take in each direction.

    Note: The file may contain empty lines, which should be ignored.

    Args:
    file_name (str): The pathname of the file containing the map data.

    Returns:
    tuple: A tuple containing two elements:
        - The first element is a tuple (x, y) representing the starting
          coordinates.
        - The second element is a list of tuples, where each tuple contains:
            - A direction (str): 'N' for North, 'E' for East, 'S' for South,
              or 'W' for West.
            - The number of steps (int) to take in that direction.

    >>> read_map("treasure_3.txt")
    ((0, 11), \
[('W', 5), ('W', 6), ('S', 7), ('E', 3), ('E', 4), \
('N', 5), ('E', 2), ('S', 2), ('E', 2), ('N', 4)])
    """
    with open(file_name, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    x, y = data[0].strip().split()

    direction = 'N'
    mapa = []
    for line in data[1:]:
        if not line:
            continue
        azimuth, steps = line.strip().split()
        direction = define_direction(direction, int(azimuth))

        mapa.append((direction, int(steps)))

    return ((int(x), int(y)), mapa)


def find_path(start:tuple, treasure_directions:list[tuple]) -> list[tuple]:
    """
    Calculates the path of coordinates based on the given start position
    and a series of directional steps. The start position is provided as
    a tuple of coordinates (x, y).

    The function interprets movement based on the following directional
    rules, with steps determining how far to move in a given direction:
    - 'W' (West): decreases the y-coordinate (moves left).
    - 'E' (East): increases the y-coordinate (moves right).
    - 'N' (North): decreases the x-coordinate (moves up).
    - 'S' (South): increases the x-coordinate (moves down).

    Args:
    start (tuple): A tuple representing the starting coordinates (x, y).
    treasure_directions (list of tuple): A list of tuples where each tuple
                                         contains:
                                         - A direction ('N', 'E', 'W', 'S')
                                         - An integer representing the number
                                           of steps to take in that direction.

    Returns:
    list of tuple: A list of coordinates (x, y) representing the path taken 
                   from the start position, including all intermediate steps.

    >>> start = (0, 0)
    >>> path = [('E', 3), ('S', 3), ('W', 3), ('N', 3)]
    >>> find_path(start, path)
    [(0, 0), \
(0, 1), (0, 2), (0, 3), \
(1, 3), (2, 3), (3, 3), \
(3, 2), (3, 1), (3, 0), \
(2, 0), (1, 0), (0, 0)\
]
    """
    x, y = start

    map_steps = [(x, y)]
    for direction, steps in treasure_directions:
        if direction == 'N':
            for _ in range(steps):
                x -= 1
                map_steps.append((x, y))
        elif direction == 'S':
            for _ in range(steps):
                x += 1
                map_steps.append((x, y))
        elif direction == 'W':
            for _ in range(steps):
                y -= 1
                map_steps.append((x, y))
        elif direction == 'E':
            for _ in range(steps):
                y += 1
                map_steps.append((x, y))

    return map_steps


def find_treasure(path1:list[tuple], path2:list[tuple]) -> tuple | None:
    """
    Determines the location of the treasure based on the intersection of
    two paths. The function identifies the point of intersection and
    calculates the treasure's location based on the following conditions:

    - If the paths intersect at exactly one point, that point is the
      treasure's location.
    - If the paths intersect at exactly two points, the treasure is located
      at the midpoint between these two points. If the coordinates of the
      midpoint are fractional, they are rounded down to the nearest integer.
    - If the paths intersect at more than two points, it is impossible
      to determine the treasure's exact location, and the function
      returns `None`.

    Args:
    path1 (list of tuple): The first path, represented as
                           a list of coordinates (x, y).
    path2 (list of tuple): The second path, represented as
                           a list of coordinates (x, y).

    Returns:
    tuple or None: The coordinates (x, y) of the treasure if it
    can be determined, or `None`  if the treasure's location
    cannot be identified.

    >>> path1 = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0), (0, 0)]
    >>> path2 = [(2, 4), (2, 3), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)]
    >>> path3 = [(1, 4), (1, 3), (1, 2), (2, 2), (3, 2), (3, 3), (3, 4), (2, 4), (1, 4)]
    >>> find_treasure(path1, path2)
    (2, 2)
    >>> find_treasure(path1, path3)
    (1, 2)
    >>> find_treasure(path2, path3)
    """

    intersection = list(set(path1) & set(path2))

    if len(intersection) == 1:
        return intersection[0]
    if len(intersection) == 2:
        x1, y1 = intersection[0]
        x2, y2 = intersection[1]
        return ((x1 + x2) // 2, (y1 + y2) // 2)
    return None


def find_size(path:list[tuple]) -> tuple:
    """
    Calculates the size of the map based on the given path. The size of the map
    is determined by the minimal number of points needed vertically and
    horizontally to encompass the entire path. The height is the difference
    between the maximum and minimum x-coordinates, and the width is the
    difference between the maximum and minimum y-coordinates.

    Args:
    path (list of tuple): A list of coordinates (x, y) representing the path.

    Returns:
    tuple: A tuple (height, width) where:
        - height is the number of points needed vertically.
        - width is the number of points needed horizontally.

    >>> path = [(2, 4), (2, 3), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)]
    >>> find_size(path)
    (3, 3)
    """
    min_x = path[0][0]
    max_x = path[0][0]
    min_y = path[0][1]
    max_y = path[0][1]

    for x, y in path:
        max_x = max(x, max_x)
        max_y = max(y, max_y)
        min_x = min(x, min_x)
        min_y = min(y, min_y)

    height = (max_x - min_x) + 1
    width = (max_y - min_y) + 1

    return (height, width)


def shift_path(path:list[tuple]) -> tuple:
    """
    Shifts the given path to ensure that all coordinates are non-negative
    and the smallest coordinate is positioned at (0, 0).

    The function returns a tuple, where the first element is a tuple
    containing the minimum y and x values before the shift, and the second
    element is the list of shifted coordinates.

    Args:
    path (list of tuple): A list of tuples where each tuple represents a
                          coordinate (x, y) along the path.

    Returns:
    tuple: A tuple where:
        - The first element is a tuple representing the minimum
          y-coordinate and x-coordinate found in the path.
        - The second element is a list of tuples representing the shifted path,
          where all coordinates are non-negative.

    >>> path = [(2, 4), (2, 3), (2, 2), (3, 2), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4)]
    >>> shift_path(path)
    ((2, 2), [(0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2)])
    """

    min_x = path[0][0]
    min_y = path[0][1]

    for x, y in path:
        min_x = min(x, min_x)
        min_y = min(y, min_y)

    corrected_path = []
    for path_x, path_y in path:
        path_x -= min_x
        path_y -= min_y
        corrected_path.append((path_x, path_y))

    return ((min_x, min_y), corrected_path)


def decode_map(file_name1:str, file_name2:str, map_file_name:str) -> None:
    """
    Draws a map that visualizes two paths and the treasure (if it exists)
    based on the paths provided in two input files. The map is written
    to the specified output file.

    - The paths are marked with `.`.
    - The start of the first path is marked with `1`.
    - The start of the second path is marked with `2`.
    - If the start of the first and second path coincides, it is
      marked with `3`.
    - If the treasure is found (i.e., the paths intersect at a specific point),
      it is marked with `x`. The treasure marker `x` overwrites the start
      markers '1' and '2' if they coincide with the treasure's location.

    Args:
    file_name1 (str): The name of the file containing the first path.
    file_name2 (str): The name of the file containing the second path.
    map_file_name (str): The name of the output file where the map will be drawn.

    Returns:
    None: The map is written directly to the output file.

    >>> decode_map('treasure_1.txt', 'treasure_2.txt', 'output.txt')
    >>> with open('output.txt', 'r', encoding='utf-8') as file:
    ...    print(file.read())
    1..
    . .
    ..x.2
      . .
      ...
    """

    start1, path1 = read_map(file_name1)
    start2, path2 = read_map(file_name2)

    path1 = find_path(start1, path1)
    path2 = find_path(start2, path2)

    intersection = find_treasure(path1, path2)

    # Creating list for points and finding max of them
    all_points = path1 + path2
    min_x = min(0, min(p[0] for p in all_points))
    max_x = max(0, max(p[0] for p in all_points))
    min_y = min(0, min(p[1] for p in all_points))
    max_y = max(0, max(p[1] for p in all_points))

    path1 = set(path1)
    path2 = set(path2)
    lines = []
    for i in range(min_x, max_x + 1):
        row_chars = []
        for j in range(min_y, max_y + 1):
            pos = (i, j)
            if pos == intersection:
                row_chars.append('x')
            elif pos == start1 and pos == start2:
                row_chars.append('3')
            elif pos == start1:
                row_chars.append('1')
            elif pos == start2:
                row_chars.append('2')
            elif pos in path1 or pos in path2:
                row_chars.append('.')
            else:
                row_chars.append(' ')

        lines.append("".join(row_chars).rstrip())

    with open(map_file_name, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
