"""
Graph: reading edges from a file, a dictionary representation of
an undirected graph, editing it and exporting it to the DOT format.
"""


def get_graph_from_file(filename: str) -> list[list[int]]:
    """
    Reads a graph from a specified file and returns a list of edges.
    The file should contain pairs of integers representing edges,
    with each edge formatted as "node1,node2" on a new line.
    For example:
        1,2
        3,4
        1,5

    Parameters:
    -----------
    filename: str
        The path to the file containing the graph edges in comma-separated format.

    Returns:
    --------
    list[list[int]]:
        A list of edges, where each edge is represented as a list of two integers.

    Example:
    --------
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('1,2\\n3,4\\n1,5\\n')
    >>> get_graph_from_file(tmp.name)
    [[1, 2], [3, 4], [1, 5]]
    >>> os.remove(tmp.name)
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('1,2\\n3,4\\n1,5\\n \\n')
    >>> get_graph_from_file(tmp.name)
    [[1, 2], [3, 4], [1, 5]]
    >>> os.remove(tmp.name)
    """

    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    graph = []
    for line in data:
        if not line.strip():
            continue

        nodes = line.split(',')
        node1, node2 = nodes

        graph.append([int(node1), int(node2)])

    return graph


def to_edge_dict(edge_list: list[list[int]]) -> dict[int, list[int]]:
    """
    Converts a graph from a list of edges to a dictionary representation.
    Each node maps to a list of adjacent nodes based on the edges provided.
    The list of adjacent nodes should be sorted in ascending order
    and contain no duplicates.

    Parameters:
    -----------
    edge_list : list[list[int]]
        A list of edges, where each edge is represented as a list of two integers.

    Returns:
    --------
    dict[int, list[int]]:
        A dictionary with nodes as keys and lists of adjacent nodes as values.

    Example:
    --------
    >>> to_edge_dict([[1, 2], [3, 4], [1, 5], [2, 4]])
    {1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}
    """

    graph = {}

    for node1, node2 in edge_list:
        graph.setdefault(node1, []).append(node2)
        graph.setdefault(node2, []).append(node1)
    for node, neighbors in graph.items():
        graph[node] = sorted(list(set(neighbors)))

    return graph

def is_edge_in_graph(graph: dict[int, list[int]], edge: tuple[int, int]) -> bool:
    """
    Checks if a given edge exists in the graph.

    Parameters:
    -----------
    graph : dict[int, list[int]]
        A dictionary representation of the graph.
    edge : tuple[int, int]
        A tuple representing the edge to check.

    Returns:
    --------
    bool:
        True if the edge exists in the graph; False otherwise.

    Example:
    --------
    >>> is_edge_in_graph({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (3, 1))
    False
    >>> is_edge_in_graph({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (6, 1))
    False
    """

    node1, node2 = edge

    try:
        if node2 in graph[node1]:
            return True
    except KeyError:
        return False

    return False


def add_node(graph: dict[int, list[int]], node: int) -> dict[int, list[int]]:
    """
    Adds a new node to the graph and returns the updated graph.

    Parameters:
    -----------
    graph : dict[int, list[int]]
        A dictionary representation of the graph.
    node : int
        The node to add to the graph.

    Returns:
    --------
    dict[int, list[int]]:
        The updated graph with the new node included.

    Example:
    --------
    >>> add_node({1: [2], 2: [1]}, 3)
    {1: [2], 2: [1], 3: []}
    """

    if node in graph:
        return graph

    graph[node] = []
    return graph


def del_node(graph: dict[int, list[int]], node: int) -> dict[int, list[int]]:
    """
    Deletes a node and all its incident edges from the graph.

    Parameters:
    -----------
    graph : dict[int, list[int]]
        A dictionary representation of the graph.
    node : int
        The node to delete from the graph.

    Returns:
    --------
    dict[int, list[int]]:
        The updated graph with the specified node and its edges removed.

    Example:
    --------
    >>> del_node({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, 4)
    {1: [2, 5], 2: [1], 3: [], 5: [1]}
    """

    if node not in graph:
        return graph

    del graph[node]

    for _, ends in graph.items():
        if node in ends:
            ends.remove(node)

    return graph


def add_edge(graph: dict[int, list[int]], edge: tuple[int, int]) -> dict[int, list[int]]:
    """
    Adds a new edge to the graph and returns the updated graph.

    Parameters:
    -----------
    graph : dict[int, list[int]]
        A dictionary representation of the graph.
    edge : tuple[int, int]
        A tuple representing the edge to add.

    Returns:
    --------
    dict[int, list[int]]:
        The updated graph with the new edge included.

    Example:
    --------
    >>> add_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (1, 3))
    {1: [2, 5, 3], 2: [1, 4], 3: [4, 1], 4: [2, 3], 5: [1]}
    >>> add_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (6, 7))
    {1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1], 6: [7], 7: [6]}
    """

    if is_edge_in_graph(graph, edge):
        return graph

    node1, node2 = edge

    if node1 not in graph or node2 not in graph:
        graph = add_node(graph, node1)
        graph = add_node(graph, node2)

    graph.setdefault(node1, []).append(node2)
    graph.setdefault(node2, []).append(node1)

    return graph


def del_edge(graph: dict[int, list[int]], edge: tuple[int, int]) -> dict[int, list[int]]:
    """
    Removes an edge from the graph and returns the updated graph.

    Parameters:
    -----------
    graph : dict[int, list[int]]
        A dictionary representation of the graph.
    edge : tuple[int, int]
        A tuple representing the edge to remove.

    Returns:
    --------
    dict[int, list[int]]:
        The updated graph with the specified edge removed.

    Example:
    --------
    >>> del_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (2, 4))
    {1: [2, 5], 2: [1], 3: [4], 4: [3], 5: [1]}
    >>> del_edge({1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}, (7, 4))
    {1: [2, 5], 2: [1, 4], 3: [4], 4: [2, 3], 5: [1]}
    """

    if not is_edge_in_graph(graph, edge):
        return graph

    node1, node2 = edge

    if node1 not in graph or node2 not in graph:
        return graph

    graph[node1].remove(node2)
    graph[node2].remove(node1)

    return graph


def convert_to_dot(filename: str) -> None:
    """
    Reads a file of edges, converts it into a directed graph in DOT format,
    and saves it as a file with the same name but with a .dot extension.

    This function allows for quick visualization and verification of
    graph functions by exporting them in a format that can be rendered as a graph.

    Parameters:
    -----------
    filename : str
        The name of the input file containing graph edges in "node1,node2" format,
        with one edge per line.

    Returns:
    --------
    None
        Saves the directed graph in DOT format to a file with the same
        name as the input file but with a .dot extension.
        Every edge "a,b" becomes two arcs: "a -> b" and "b -> a".

    Example:
    --------
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('1,2\\n3,4\\n1,5\\n')
    >>> convert_to_dot(tmp.name)
    >>> dot_name = tmp.name[:-len('.txt')] + '.dot'
    >>> with open(dot_name, encoding='utf-8') as dot_file:
    ...     print(dot_file.read().strip())
    digraph {
    1 -> 2
    1 -> 5
    2 -> 1
    3 -> 4
    4 -> 3
    5 -> 1
    }
    >>> os.remove(tmp.name)
    >>> os.remove(dot_name)
    """

    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    edges = set()

    for line in data:
        nodes = line.split(',')
        node1, node2 = nodes

        edges.add((node1, node2))
        edges.add((node2, node1))

    filename = filename.rsplit('.')[0] + '.dot'

    diagraph_content = ['digraph {']
    for node1, node2 in sorted(edges):
        diagraph_content.append(f'{node1} -> {node2}')
    diagraph_content.append('}')

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(diagraph_content))


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
