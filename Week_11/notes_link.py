"""
Модуль notes_link: граф зв'язків між нотатками у стилі Obsidian.
"""

def build_graph_from_note(note_path: str, graph: dict | None = None) -> dict:
    """
    Build the graph of all notes reachable from the note at note_path.

    A link to a note looks like [[name]] and means a link to the file
    name.md in the same folder. The result is a dictionary
    {note name: sorted list of unique names it links to}.
    Notes without links are not keys of the dictionary.
    A link to a note that does not exist is kept, but not followed.
    If graph is given, the new notes are added to it.
    The function must call itself.

    >>> build_graph_from_note('./note.md')
    {'note': ['note1'], 'note1': ['note2'], 'note2': ['note3'], \
'note3': ['note', 'note4'], 'note4': ['note23', 'note5']}
    >>> previous_notes = {'cake recipe': ['sugar', 'flour', 'eggs'], 'hello': ['hiii']}
    >>> build_graph_from_note('note.md', previous_notes)
    {'cake recipe': ['sugar', 'flour', 'eggs'], 'hello': ['hiii'], \
'note': ['note1'], 'note1': ['note2'], 'note2': ['note3'], \
'note3': ['note', 'note4'], 'note4': ['note23', 'note5']}
    """

    dir_prefix = ''

    if graph is None:
        graph = {}

    if not note_path.endswith('.md'):
        note_path += '.md'

    try:
        with open(note_path, 'r', encoding='utf-8') as file:
            link_set = set()
            for line in file:
                while line.find('[[') != -1 and line.find(']]') != -1:
                    left = line.find('[[')
                    right = line.find(']]', left)
                    if left != -1 and right != -1:
                        new_line = line[left+2:right]
                        link_set.add(new_line)
                        lenght = len(new_line)
                        line = line[line.find(f'[[{new_line}]]')+lenght+2:]
    except FileNotFoundError:
        return graph

    if '/' in note_path:
        dir_prefix = note_path[:note_path.rfind('/')+1]
        note_path = note_path[note_path.rfind('/')+1:]

    if link_set:
        graph[note_path[:-3]] = sorted(list(link_set))

    for link in link_set:
        if link in graph:
            continue

        new_note = build_graph_from_note(f'{dir_prefix}{link}', graph)

        graph.update(new_note)

    return graph


def convert_to_dot(graph: dict) -> None:
    """
    Write the graph to the file graph.dot in the DOT format:
    the line 'digraph {', then one line 'note -> link' for every link
    (notes in sorted order, links in the order of their list), then '}'.

    >>> graph = {'cake recipe': ['sugar', 'flour', 'eggs'], 'hello': ['hiii'], 'note2': ['note3'], \
'note': ['note1'], 'note1': ['note2'], 'note3': ['note']}
    >>> convert_to_dot(graph)
    >>> with open('graph.dot', 'r', encoding='utf-8') as file:
    ...     print(file.read())
    digraph {
    cake recipe -> sugar
    cake recipe -> flour
    cake recipe -> eggs
    hello -> hiii
    note -> note1
    note1 -> note2
    note2 -> note3
    note3 -> note
    }
    """
    key_list = sorted(graph.keys())

    with open('graph.dot', 'w', encoding='utf-8') as file:
        file.write('digraph {\n')
        for k in key_list:
            value_list = graph.get(k)
            for item in value_list:
                file.write(f'{k} -> {item}\n')
        file.write('}')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
