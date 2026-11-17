"""
Advent of code
"""

def read_map(pathname:str) -> tuple[str, dict]:
    """
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write("LLR\\n\\nAAA = (BBB, BBB)\\nBBB = (AAA, ZZZ)\\n \
ZZZ = (ZZZ, ZZZ)\\n")
    >>> read_map(tmp.name)
    ('LLR', {'AAA': ('BBB', 'BBB'), 'BBB': ('AAA', 'ZZZ'), 'ZZZ': ('ZZZ', 'ZZZ')})
    >>> os.remove(tmp.name)
    """

    with open(pathname, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    directions = data[0]

    nodes = {}
    for line in data[1:]:
        if not line:
            continue
        start, ends = line.split('=')
        left_end, right_end = ends[2:-1].split(',')

        nodes[start.strip()] = (left_end, right_end.strip())

    return (directions, nodes)


def navigation_through_desert(directions:str, nodes:dict) -> int:
    """
    >>> directions = 'LLR'
    >>> nodes = {'AAA': ('BBB', 'BBB'),
    ...        'BBB': ('AAA', 'ZZZ'),
    ...        'ZZZ': ('ZZZ', 'ZZZ')}
    >>> navigation_through_desert(directions, nodes)
    6
    """
    step = 0
    point = 'AAA'
    while point != 'ZZZ':
        for char in directions:
            if char == 'L':
                point = nodes.get(point, None)[0]
            else:
                point = nodes.get(point, None)[1]
            step += 1

    return step


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    directions_global, nodes_dict = read_map('map.txt')
    steps = navigation_through_desert(directions_global, nodes_dict)
    print(steps)
