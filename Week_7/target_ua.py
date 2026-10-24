"""
Target UA - a word game with Ukrainian words.

The player gets 5 unique Ukrainian letters and a part of speech, and
must name words (up to 5 letters long) of that part of speech that
start and end with one of the given letters.
"""

from random import choice, sample

def generate_grid() -> list[str]:
    """
    Generates a list of 5 unique lowercase Ukrainian letters.

    Returns:
        list[str]: 5 unique letters of the Ukrainian alphabet.
                   Example: ['ґ', 'ь', 'й', 'є', 'ї']

    Examples:
    >>> letters = generate_grid()
    >>> len(letters)
    5
    >>> len(sorted(letters)) == len('абвгґ')
    True
    """

    ukrainian_alphabet = "абвгґдеєжзиіїйклмнопрстуфхцчшщьюя"

    # Sample returns unique elements
    return sample(ukrainian_alphabet, 5)


def get_words(pathname: str, letters: list[str]) -> list[tuple[str, str]]:
    """
    Reads the dictionary file and returns (word, part_of_speech) pairs
    that match the game rules.

    Dictionary line format: a word, whitespace, then a grammar tag,
    e.g. "абажур /n20.a.p.ke", "аакуватий /adj", "дибки adv".
    The tag (with or without the leading '/') maps to a part of speech:
    'adj...' -> 'adjective', 'adv...' -> 'adverb', 'v...' -> 'verb',
    'noun...' -> 'noun', and 'n' or 'np' followed by a digit -> 'noun'
    (e.g. 'n20.a.p', 'np3'). If a tag lists several parts ("adj.adv"),
    only the first one is used. Lines with any other tags (noninfl,
    numr, conj, prep, ...) are skipped.

    Word selection rules:
    1. Word is at most 5 characters long
    2. Word starts AND ends with one of the letters (they may coincide)
    3. Word's part of speech is one of the four listed above
    Pairs are returned in the order the words appear in the file.

    Args:
        pathname (str): Path to the dictionary file.
        letters (list[str]): 5 lowercase letters of the game grid.

    Returns:
        list[tuple[str, str]]: Pairs (word, part_of_speech).

    Examples:
    >>> import tempfile, os
    >>> content = 'ґедзь /n20.a\\nїдкий /adj.adv\\nдибки adv\\nдіяти /v1\\nщось /pron\\n'
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
    ...     _ = tmp.write(content)
    >>> get_words(tmp.name, ['ґ', 'ь', 'й', 'ї', 'и'])
    [('ґедзь', 'noun'), ('їдкий', 'adjective')]
    >>> get_words(tmp.name, ['д', 'и', 'в', 'а', 'я'])
    [('дибки', 'adverb'), ('діяти', 'verb')]
    >>> os.remove(tmp.name)
    """

    words = []

    with open(pathname, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.split()

            if len(line) < 2:
                continue

            word, lan_part = line[0], line[1]

            if len(word) > 5 or not (word[0] in letters and word[-1] in letters):
                continue

            lan_part = lan_part.replace('/', '')
            allowed_lan_parts = ('adv', 'adj', 'n', 'v')
            for check_part in allowed_lan_parts:
                if (lan_part.startswith(check_part) and
                not ('numr' in lan_part or 'noninfl' in lan_part)):
                    match check_part:
                        case 'adv':
                            check_part = 'adverb'
                        case 'adj':
                            check_part = 'adjective'
                        case 'n':
                            check_part = 'noun'
                        case 'v':
                            check_part = 'verb'

                    if check_part:
                        words.append((word, check_part))

    return words

def get_user_words() -> list[str]:
    """
    Reads words from user input until EOF signal is received.

    The user enters one word per line. Input is terminated by pressing:
    - Unix/Linux/Mac: Ctrl+D
    - Windows: Ctrl+Z, then Enter

    Returns:
        list[str]: List of words entered by the user.

    Note:
        This function does not print any messages to the screen. All
        instructions for the user should be displayed in the main()
        function.
    """
    user_words = []

    try:
        while True:
            user_words.append(input('Введіть слова (завершення — Ctrl+D):'))
    except EOFError:
        return user_words


def check_user_words(user_words: list[str], language_part: str,
                     letters: list[str], vocabulary: str) -> tuple[list[str], list[str]]:
    """
    Checks user words against the game rules and the dictionary.

    A user word is correct if the pair (word, language_part) matches
    the game rules for the given letters and is present in the
    vocabulary file. Missed words are the dictionary words of the given
    part of speech that match the rules but were not named by the user.

    Args:
        user_words (list[str]): Words entered by the user.
        language_part (str): One of 'noun', 'verb', 'adjective', 'adverb'.
        letters (list[str]): 5 lowercase letters of the game grid.
        vocabulary (str): Path to the dictionary file.

    Returns:
        tuple[list[str], list[str]]: (correct user words, missed words).

    Examples:
    >>> import tempfile, os
    >>> content = 'ґедзь /n20.a\\nїдкий /adj.adv\\nїнь /n20\\nдіяти /v1\\n'
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
    ...     _ = tmp.write(content)
    >>> check_user_words(['ґедзь', 'їжак'], 'noun', ['ґ', 'ь', 'й', 'ї', 'и'], tmp.name)
    (['ґедзь'], ['їнь'])
    >>> check_user_words([], 'adjective', ['ґ', 'ь', 'й', 'ї', 'и'], tmp.name)
    ([], ['їдкий'])
    >>> os.remove(tmp.name)
    """

    dict_words = get_words(vocabulary, letters)

    valid_dict_words =  [word for word, speech_part in dict_words if speech_part == language_part]

    correct_words = []

    for word in user_words:
        if word not in correct_words and word in valid_dict_words:
            correct_words.append(word)

    missed_words = [word for word in valid_dict_words if word not in correct_words]

    return correct_words, missed_words


def main():
    """
    Main function of the Target UA game.

    Implements the complete game scenario:
    1. Generates and displays 5 unique Ukrainian letters
    2. Randomly picks and displays a part of speech
       ('noun', 'verb', 'adjective', 'adverb')
    3. Displays a prompt and reads words from the player
    4. Displays the number of correct words and the list of them
    5. Displays the words that the player missed
    """

    # 1. Generates and displays 5 unique Ukrainian letters
    grid = generate_grid()
    print(f'Ваші літери: {' '.join(grid)}')

    # 2. Randomly picks and displays a part of speech
    parts_of_speech = ('noun', 'verb', 'adjective', 'adverb')
    part_of_speech = choice(parts_of_speech)
    print(f'Частина мови: {part_of_speech}')

    # 3. Displays a prompt and reads words from the player
    user_words =  get_user_words()

    # 4. Displays the number of correct words and the list of them
    correct_words, misssed_words = check_user_words(user_words, part_of_speech, grid, 'base.lst')
    print(f'Правильних слів: {len(correct_words)}')
    print(f'Ваші правильні слова: {correct_words}')

    # 5. Displays the words that the player missed
    print(f'Пропущені слова: {misssed_words}')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    main()
