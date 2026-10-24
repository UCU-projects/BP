"""
Target Game - a word search game using letters from the game grid.

The player must find as many words as possible (minimum 4 letters) using
letters from a 3x3 grid. Each word must contain the central letter.
"""

from random import randint

def generate_grid() -> list[list[str]]:
    """
    Generates a 3x3 grid of uppercase letters for the game.

    The grid should contain 3 vowels and 6 consonants for optimal game
    balance.

    Returns:
        list[list[str]]: A list of 3 lists, each containing 3 uppercase letters.
                         Example: [['E', 'T', 'O'], ['O', 'P', 'N'], ['P', 'U', 'R']]

    Examples:
    >>> grid = generate_grid()
    >>> len(grid)
    3
    >>> [len(row) for row in grid]
    [3, 3, 3]
    >>> len([letter for row in grid for letter in row])
    9
    """
    vowels =  ['A', 'E', 'I', 'O', 'U']
    consonants = [chr(ord('A') + char) for char in range(26) if chr(ord('A') + char) not in vowels]

    vowel_count = 0
    consonants_count = 0

    grid = []

    for _ in range(3):
        row = []
        for _ in range(3):
            if randint(1, 3) == 1 and vowel_count < 3 or consonants_count == 6:
                row.append(vowels[randint(0, len(vowels)-1)])
                vowel_count += 1
            elif consonants_count < 6:
                row.append(consonants[randint(0, len(consonants)-1)])
                consonants_count += 1

        grid.append(row)

    return grid


def get_words(pathname: str, letters: list[str]) -> list[str]:
    """
    Reads the dictionary file and returns words that match the game rules.

    Word selection rules:
    1. Word must contain at least 4 letters
    2. Word must contain the central letter
    3. Each letter in the word is used no more times than it appears on the grid
    4. All letters in the word must be present on the grid
    5. Words are returned in lowercase

    Args:
        pathname (str): Path to the dictionary file
        letters (list[str]): List of 9 letters from the game grid in lowercase.
                             Element at index 4 is the central letter (mandatory).
                             Example: ['e', 't', 'o', 'o', 'p', 'n', 'p', 'u', 'r']

    Returns:
        list[str]: List of words from the dictionary that match all rules.

    Examples:
        >>> get_words('en.txt', ['w', 'u', 'm', 'r', 'o', 'v', 'k', 'i', 'f'])[:8]
        ['fork', 'form', 'forum', 'four', 'fowk', 'from', 'frow', 'irok']
        >>> len(get_words('en.txt', ['w', 'u', 'm', 'r', 'o', 'v', 'k', 'i', 'f']))
        16
        >>> words = get_words('en.txt', ['e', 't', 'o', 'o', 'p', 'n', 'p', 'u', 'r'])
        >>> [word for word in words if 'p' not in word]
        []
        >>> [word for word in words if len(word) < 4]
        []
    """

    dict_words = []

    with open(pathname, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip().lower()

            if line in dict_words:
                continue

            if len(line) < 4 or letters[4] not in line:
                continue

            for letter in line:
                if line.count(letter) > letters.count(letter):
                    break
            else:
                dict_words.append(line.strip().lower())

    return dict_words


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
        instructions for the user should be displayed in the main() function.
    """
    user_words = []
    try:
        while True:
            user_words.append(input('Введіть слова (завершення — Ctrl+D):'))
    except EOFError:
        return user_words


def get_pure_user_words(user_words: list[str], letters: list[str],
                        words_from_dict: list[str]) -> list[str]:
    """
    Checks user words and returns those that match game rules but are not in the dictionary.

    This function helps identify words that the user entered correctly according
    to the game rules (length >= 4, contain central letter, all letters are on
    the grid), but which were not found in the game dictionary. These could be
    spelling errors or rare words.

    Args:
        user_words (list[str]): Words entered by the user.
        letters (list[str]): List of 9 letters from the game grid (lowercase).
                             Element [4] is the central letter.
        words_from_dict (list[str]): Words from the dictionary that match the rules.

    Returns:
        list[str]: List of user words that match game rules but are not found
                   in the dictionary.

    Examples:
        >>> letters = ['i', 'g', 'e', 'p', 'i', 's', 'w', 'm', 'g']
        >>> get_pure_user_words(['impi', 'gipm'], letters, ['work', 'worm'])
        ['impi', 'gipm']
        >>> get_pure_user_words(['test'], ['i', 'g', 'e', 'p', 'i', 's', 'w', 'm', 'g'], [])
        []
        >>> get_pure_user_words(['pig'], ['p', 'i', 'g', 'e', 'p', 's', 'w', 'm', 'g'], [])
        []
    """

    legal_words = []

    for word in user_words:
        if len(word) < 4 or letters[4] not in word:
            continue

        for letter in word:
            if word.count(letter) > letters.count(letter):
                break
        else:
            legal_words.append(word)

    dict_copy = words_from_dict.copy()
    remaining_legal = []

    for word in legal_words:
        if word in dict_copy:
            dict_copy.remove(word)
        else:
            remaining_legal.append(word)

    return remaining_legal


def main():
    """
    Main function of the Target game.

    Implements the complete game scenario:
    1. Generates and displays a 3x3 game grid
    2. Displays a prompt and reads words from the player
    3. Gets all possible words from the dictionary
    4. Displays the number of correct words from the user
    5. Displays all possible words from the dictionary
    6. Displays words that the player missed
    7. Displays player's words that are not in the dictionary
    """

    # 1. Generates and displays a 3x3 game grid
    grid = generate_grid()
    print('\n'.join([' '.join(row) for row in grid]))

    letters_up = []
    for row in grid:
        letters_up.extend(row)

    letters = []
    for letter in letters_up:
        letters.append(letter.lower())

    # 2. Displays a prompt and reads words from the player
    user_words = get_user_words()

    # 3. Gets all possible words from the dictionary
    dict_words = get_words('en.txt', letters)

    # 4. Displays the number of correct words from the user
    correct_user_words = [word for word in user_words if word in dict_words]
    print(f'Правильних слів: {len(correct_user_words)}')

    #5. Displays all possible words from the dictionary
    print(f'Усі можливі слова: {dict_words}')

    #6. Displays words that the player missed
    missed_words = [word for word in dict_words if word not in user_words]
    print(f'Пропущені слова: {missed_words}')

    #7. Displays player's words that are not in the dictionary
    out_of_bounds = get_pure_user_words(user_words, letters, dict_words)
    print(f'Слова поза словником: {out_of_bounds}')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    main()
