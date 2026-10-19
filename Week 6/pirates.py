"""
Lab work 6
Creating maps and knowing we are rich
"""

def find_path(treasure_map: list) -> list:
    """
    Finds the path in coordinates according to treasure_map
    assuming that start is in (0, 0).
    If we go left by 1 from the start, the coordinate is (0, -1).
    If right – (0, 1).
    If we go up by 1 from the start, the coordinate is (-1, 0).
    If down – (1, 0).

    :param treasure_map: list, A list of tuples representing commands for navigating treasure path   
    :return: list, A list of tuples with real coordinates by step.

    >>> map = [('U', 2), ('R', 2), ('D', 2), ('R', 2), \
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> find_path(map)
    [(0, 0), (-1, 0), (-2, 0), (-2, 1), (-2, 2), \
(-1, 2), (0, 2), (0, 3), (0, 4), (-1, 4), (-2, 4), \
(-3, 4), (-4, 4), (-4, 3), (-4, 2), (-4, 1), (-4, 0), \
(-4, -1), (-4, -2), (-4, -3), (-4, -4), (-4, -5), \
(-4, -6), (-4, -7), (-3, -7), (-2, -7), (-1, -7), \
(0, -7), (1, -7), (2, -7), (3, -7), (3, -6), \
(3, -5), (3, -4), (3, -3), (3, -2), (3, -1), \
(3, 0), (2, 0), (1, 0), (0, 0)]
    """
    result = [(0, 0)]

    for command in treasure_map:
        how_much = command[1]

        if command[0] == 'U':
            for _ in range(how_much):
                result.append((result[-1][0] - 1, result[-1][1]))
        elif command[0] == 'D':
            for _ in range(how_much):
                result.append((result[-1][0] + 1, result[-1][1]))
        elif command[0] == 'R':
            for _ in range(how_much):
                result.append((result[-1][0], result[-1][1] + 1))
        elif command[0] == 'L':
            for _ in range(how_much):
                result.append((result[-1][0], result[-1][1] - 1))

    return result


def find_positive_path(path: list) -> list:
    '''Find the path with nonnegative coordinates by shifting
    the path horizontally and vertically by minimal steps.

    :param path: list, A list of tuples representing commands for navigating treasure path
    :return: list, A list of tuples with map coordinates by step. 

    >>> treasure_map = [('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> path = find_path(treasure_map)
    >>> find_positive_path(path)
    [(4, 7), (3, 7), (2, 7), (2, 8), (2, 9), (3, 9), \
(4, 9), (4, 10), (4, 11), (3, 11), (2, 11), (1, 11), \
(0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), \
(0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), \
(3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (7, 1), (7, 2), \
(7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (6, 7), (5, 7), (4, 7)]
    '''

    result = []

    min_x = 0
    min_y = 0
    for coordinate in path:
        if coordinate[0] < min_y:
            min_y = coordinate[0]

        if coordinate[1] < min_x:
            min_x = coordinate[1]

    if min_x == 0 and min_y == 0:
        return path

    for coordinate in path:
        result.append((coordinate[0] - min_y, coordinate[1] - min_x))

    return result


def find_size(path: list) -> tuple:
    '''Finds the size of the map: minimal number of points vertically
    and horizontally needed to build the path. Return tuple where the
    first coordinate is the height of the map and the second is the length.

    :param path: list, A list of tuples with map coordinates by step. 
    :return: tuple, A tuple with two integers representing height and length 

    >>> treasure_map = [('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> find_size(find_positive_path(find_path(treasure_map)))
    (8, 12)
    '''

    max_x = 0
    max_y = 0
    for coordinate in path:
        if coordinate[0] > max_y:
            max_y = coordinate[0]

        if coordinate[1] > max_x:
            max_x = coordinate[1]

    # Because we accounting zero as number
    return (max_y + 1, max_x + 1)


def view_map(path: list) -> str:
    '''
    From path creates the map. Returns string representation of the map.
    If the coordinate is on the path, put the symbol 'x'.
    Otherwise use '.'.

    :param path: list, A list of tuples with real coordinates by step.
    :return: str, A couple of strings representing map

    >>> treasure_map = [('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> path = find_path(treasure_map)
    >>> view_map(path)
    'xxxxxxxxxxxx\\n\
x..........x\\n\
x......xxx.x\\n\
x......x.x.x\\n\
x......x.xxx\\n\
x......x....\\n\
x......x....\\n\
xxxxxxxx....'
    '''
    path = find_positive_path(path)
    y, x = find_size(path)

    map_ = ''

    for i in range(y):
        for j in range(x):
            if (i, j) in path:
                map_ += 'x'
                continue
            map_ += '.'

        if i == y - 1:
            continue

        map_ += '\n'

    return map_

def find_vertices(treasure_map: list) -> list:
    '''Find the vertices of polygon that created on our map.

    :param treasure_map: list, A list of tuples representing commands for navigating treasure path   
    :return: list, A list of tuples with real coordinates of vertices.

    >>> treasure_map = [('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> find_vertices(treasure_map)
    [(-2, 0), (-2, 2), (0, 2), (0, 4), (-4, 4), (-4, -7), (3, -7), (3, 0)]
    >>> treasure_map = [('U', 2), ('R', 2), ('R', 2), ('D', 2), ('L', 4)]
    >>> find_vertices(treasure_map)
    [(0, 0), (-2, 0), (-2, 4), (0, 4)]
    '''
    merged = []
    previous = (0, 0)

    for command in treasure_map:
        if command[0] == previous[0]:
            merged.pop(-1)
            merged.append((previous[0], command[1] + previous[1]))
        else:
            merged.append(command)
        previous = command

    result = [(0, 0)]
    for command in merged:
        how_much = command[1]

        if command[0] == 'U':
            result.append((result[-1][0] - how_much, result[-1][1]))
        elif command[0] == 'D':
            result.append((result[-1][0] + how_much, result[-1][1]))
        elif command[0] == 'R':
            result.append((result[-1][0], result[-1][1] + how_much))
        elif command[0] == 'L':
            result.append((result[-1][0], result[-1][1] - how_much))

    if treasure_map[0][0] == treasure_map[-1][0]:
        result.pop(-1)

    if result[0] == result[-1]:
        result.pop(-1)

    if merged[0][0] == merged[-1][0] and result[0] == (0, 0):
        result.pop(0)

    return result


def calculate_polygon_area(vertices: list) -> int:
    '''
    Calculate the polygon area using the list of vertices of the
    polygon.

    :param vertices: list, A list of tuples with real coordinates of vertices.
    :return: int, An area of polygon represented by integer

    >>> vertices = find_vertices([('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)])
    >>> calculate_polygon_area(vertices)
    61
    '''
    n = len(vertices)
    area = 0

    for i in range(n):
        y1, x1 = vertices[i]
        y2, x2 = vertices[(i + 1) % n]
        area += (y1 * x2) - (y2* x1)

    return abs(area) // 2


def find_volume_treasure(area: int, length: int) -> int:
    '''
    Find the number of interior points. Each point is one treasure.

    :param area: int, An area of polygon represented by integer
    :param lenght: int, A length of the path by step
    :return: int, A volume of found tresure

    >>> treasure_map = [('U', 2), ('R', 2), ('D', 2), ('R', 2),\
('U', 4), ('L', 11), ('D', 7), ('R', 7), ('U', 3)]
    >>> vertices = find_vertices(treasure_map)
    >>> area = calculate_polygon_area(vertices)
    >>> length = len(find_path(treasure_map))-1
    >>> find_volume_treasure(area, length)
    42
    '''

    return area + 1 - length // 2


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
