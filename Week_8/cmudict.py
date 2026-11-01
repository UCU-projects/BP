"""
CMU pronouncing dictionary: reading it from a file into a list or
a dictionary and grouping words by the number of their pronunciations.
"""


def dict_reader_tuple(file_dict: str) -> list[tuple[str, int, list[str]]]:
    """
    Reads a pronunciation dictionary file and returns a list of tuples.

    Each line of the file holds a word, the number of its pronunciation
    variant and the phonemes, separated by spaces, e.g.
        NACHOS 2 N AE1 CH OW0 Z
    Every line becomes a tuple (word, variant, phonemes), where word is
    a str, variant is an int and phonemes is a list of str. The tuples
    go in the same order as the lines in the file.

    Parameters:
    -----------
    file_dict : str
        The path to the pronunciation dictionary file.

    Returns:
    --------
    list[tuple[str, int, list[str]]]:
        A list of tuples (word, variant number, phonemes).

    Example:
    --------
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('A 1 AH0\\nA. 1 EY1\\nA 2 EY1\\nNACHOS 1 N AA1 CH OW0 Z\\n')
    >>> dict_reader_tuple(tmp.name)[2]
    ('A', 2, ['EY1'])
    >>> dict_reader_tuple(tmp.name)[3]
    ('NACHOS', 1, ['N', 'AA1', 'CH', 'OW0', 'Z'])
    >>> len(dict_reader_tuple(tmp.name))
    4
    >>> os.remove(tmp.name)
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('A 1 AH0\\nA. 1 EY1\\nA 2 EY1\\nNACHOS 1 N AA1 CH OW0 Z\\n     ')
    >>> dict_reader_tuple(tmp.name)[2]
    ('A', 2, ['EY1'])
    >>> dict_reader_tuple(tmp.name)[3]
    ('NACHOS', 1, ['N', 'AA1', 'CH', 'OW0', 'Z'])
    >>> os.remove(tmp.name)
    """

    with open(file_dict, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    list_tuple = []
    for line in data:
        if not line.strip():
            continue

        line = line.split()

        word = line.pop(0)
        variant = int(line.pop(0))

        dict_tuple = (word, variant, line)
        list_tuple.append(dict_tuple)

    return list_tuple


def dict_reader_dict(file_dict: str) -> dict[str, set[tuple[str, ...]]]:
    """
    Reads a pronunciation dictionary file and returns a dictionary.

    Each word is a key in the dictionary, and the value is a set of
    tuples of phonemes: one tuple for each pronunciation of the word.

    Parameters:
    -----------
    file_dict : str
        The path to the pronunciation dictionary file.

    Returns:
    --------
    dict[str, set[tuple[str, ...]]]:
        A dictionary where each key is a word and the value is a set
        of phoneme tuples.

    Example:
    --------
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('A 1 AH0\\nA. 1 EY1\\nA 2 EY1\\nNACHOS 1 N AA1 CH OW0 Z\\n')
    >>> dict_reader_dict(tmp.name)['A'] == {('AH0',), ('EY1',)}
    True
    >>> dict_reader_dict(tmp.name)['NACHOS']
    {('N', 'AA1', 'CH', 'OW0', 'Z')}
    >>> len(dict_reader_dict(tmp.name))
    3
    >>> os.remove(tmp.name)
    """

    parsed_entries = dict_reader_tuple(file_dict)

    pronunciation_dict = {}

    for entry in parsed_entries:
        word = entry[0]
        phoneme_tuple = tuple(entry[2])

        if word not in pronunciation_dict:
            pronunciation_dict[word] = set()

        pronunciation_dict[word].add(phoneme_tuple)

    return pronunciation_dict


def dict_invert(dct: dict | list) -> dict[int, set[tuple[str, tuple[str, ...]]]]:
    """
    Groups the words of a pronunciation dictionary by the number of
    their pronunciations.

    The input is either a list of tuples (the result of
    dict_reader_tuple) or a dictionary (the result of dict_reader_dict).
    The result is a dictionary: each key is a number of pronunciations,
    the value is a set of tuples (word, phonemes) for all words with
    exactly that many pronunciations; phonemes are a tuple of str.
    A word with n pronunciations gives n such tuples. The keys of the
    result go in ascending order.

    Parameters:
    -----------
    dct : dict or list
        The pronunciation dictionary in dictionary or list format.

    Returns:
    --------
    dict[int, set[tuple[str, tuple[str, ...]]]]:
        A dictionary from the number of pronunciations to the set of
        (word, phonemes) tuples.

    Example:
    --------
    >>> dict_invert({'WATER': {('W', 'A', 'T', 'E', 'R')}})
    {1: {('WATER', ('W', 'A', 'T', 'E', 'R'))}}
    >>> dict_invert([('AAA', 1, ['T', 'R', 'IH2', 'P', 'AH0', 'L', 'EY1'])])
    {1: {('AAA', ('T', 'R', 'IH2', 'P', 'AH0', 'L', 'EY1'))}}
    >>> dict_invert({'AABERG': {('AA1', 'B', 'ER0', 'G')}, 'A.': {('EY1',)},
    ...              'A': {('EY1',), ('AH0',)}}) == {
    ...     1: {('A.', ('EY1',)), ('AABERG', ('AA1', 'B', 'ER0', 'G'))},
    ...     2: {('A', ('EY1',)), ('A', ('AH0',))}}
    True
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ...                                  encoding='utf-8') as tmp:
    ...     _ = tmp.write('A 1 AH0\\nA. 1 EY1\\nA 2 EY1\\nNACHOS 1 N AA1 CH OW0 Z\\n')
    >>> dict_invert(dict_reader_tuple(tmp.name)) == dict_invert(dict_reader_dict(tmp.name))
    True
    >>> os.remove(tmp.name)
    """

    unpackaged_list = {}

    if isinstance(dct, list):
        for word, _, phomene in dct:
            if word not in unpackaged_list:
                unpackaged_list[word] = set()
            unpackaged_list[word].add(tuple(phomene))
    else:
        unpackaged_list = dct

    inverted_dict = {}

    for word, phoneme_sets in unpackaged_list.items():
        pronunciation_count = len(phoneme_sets)

        if pronunciation_count not in inverted_dict:
            inverted_dict[pronunciation_count] = set()

        for phonemes in phoneme_sets:
            inverted_dict[pronunciation_count].add((word, phonemes))

    return dict(sorted(inverted_dict.items()))


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
