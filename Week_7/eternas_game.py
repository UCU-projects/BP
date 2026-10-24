"""
Eternas - a 3D "four in a row" strategy game on a circular board.

There are 16 pegs arranged in a circle; up to 4 beads can be put on
each peg. Beads are green ('g') or white ('w'); 0 marks an empty slot.
The first player to place four beads of their colour in a row
vertically, horizontally or diagonally wins, and the game stops.
"""

from random import choice, randint

def vertical_horizontal_check(board: list[list]) -> list[list[tuple[int, int]]]:
    """
    Support function for winning_combination
    Checks the board for winning vertical or horizontal combinations.

    Returns [] if there is none. Otherwise returns a list
    with winning combinations of 4 positions (level, peg)

    Args:
        board (list[list]): 16 lists of 4 items ('g', 'w' or 0).

    Returns:
        [] | list[list[tuple[int, int]]]]

    """

    combinations = []

    for peg in range(16):
        item = board[peg][0]
        if item == 0:
            continue

        for level in range(4):
            if board[peg][level] != item:
                break
        else:
            combinations.append([(level, peg) for level in range(4)])

    for level in range(4):
        for start_peg in range(16):
            pegs = [(start_peg + i) % 16 for i in range(4)]
            item = board[pegs[0]][level]

            if item == 0:
                continue

            for peg in pegs:
                if board[peg][level] != item:
                    break
            else:
                combinations.append([(level, peg) for peg in pegs])

    return combinations


def diagonally_check(board: list[list]) -> list[list[tuple[int, int]]]:
    """
    Support function for winning_combination
    Checks the board for winning diagonally down or up combinations.

    Returns [] if there is none. Otherwise returns a list
    with winning combinations of 4 positions (level, peg)

    Args:
        board (list[list]): 16 lists of 4 items ('g', 'w' or 0).

    Returns:
        [] | list[list[tuple[int, int]]]]
    """

    combinations = []

    for start_peg in range(16):
        pegs = [(start_peg + i) % 16 for i in range(4)]
        item = board[pegs[0]][0]

        if item == 0:
            continue

        for i in range(4):
            if item != board[pegs[i]][i]:
                break
        else:
            combinations.append([(i, pegs[i]) for i in range(4)])

    for start_peg in range(16):
        pegs = [(start_peg + i) % 16 for i in range(4)]
        item = board[pegs[0]][3]

        if item == 0:
            continue

        for i in range(4):
            if item != board[pegs[i]][3 - i]:
                break
        else:
            combinations.append([(3 - i, pegs[i]) for i in range(4)])

    return combinations


def winning_combination(board: list[list]) -> bool | tuple[bool, list[list[tuple[int, int]]]]:
    """
    Checks the board for winning combinations.

    Returns False if there is none. Otherwise returns a tuple
    (True, combinations) where combinations is a list of lists of
    4 positions (level, peg): level 0..3 is the index inside the peg
    list, peg 0..15 is the peg index.

    The board is circular, so horizontal and diagonal combinations
    wrap around peg 15 back to peg 0. Positions in a combination are
    listed left to right (peg index ascending along the combination)
    and top to bottom for the vertical case. Combinations are listed
    in this order: vertical, then horizontal (level by level, start
    peg ascending), then "down" diagonals (start peg ascending), then
    "up" diagonals (start peg ascending).

    Args:
        board (list[list]): 16 lists of 4 items ('g', 'w' or 0).

    Returns:
        bool | tuple[bool, list[list[tuple[int, int]]]]

    Examples:
    >>> winning_combination([['w', 'g', 'g', 'w'], [0, 0, 0, 0], [0, 'g', 'w', 'g'], \
['g', 'w', 'w', 'w'], [0, 0, 0, 'g'], [0, 0, 0, 0], [0, 0, 0, 'w'], [0, 0, 0, 0], \
[0, 0, 'w', 'w'], ['w', 'g', 'w', 'g'], [0, 0, 0, 'w'], [0, 0, 0, 'g'], [0, 0, 'g', 'w'], \
[0, 0, 0, 'w'], [0, 0, 'g', 'g'], [0, 0, 0, 'g']])
    False
    >>> winning_combination([[0, 0, 0, 'w'], [0, 0, 'w', 'w'], ['g', 'g', 'g', 'w'], \
[0, 0, 0, 'w'], ['w', 'g', 'g', 'g'], [0, 0, 0, 'g'], [0, 0, 'g', 'w'], [0, 0, 'g', 'w'], \
[0, 0, 0, 'g'], [0, 0, 0, 0], [0, 0, 0, 'w'], [0, 0, 'w', 'w'], ['g', 'g', 'w', 'g'], \
[0, 0, 0, 'w'], [0, 0, 0, 0], [0, 0, 'g', 'w']])
    (True, [[(3, 0), (3, 1), (3, 2), (3, 3)], [(3, 15), (3, 0), (3, 1), (3, 2)]])
    >>> board = [['g', 'g', 'g', 'g']] + [[0, 0, 0, 0] for _ in range(15)]
    >>> winning_combination(board)
    (True, [[(0, 0), (1, 0), (2, 0), (3, 0)]])
    """
    combinations = []

    combinations.extend(vertical_horizontal_check(board))
    combinations.extend(diagonally_check(board))

    if combinations:
        return (True, combinations)

    return False


def board_generation() -> list[list]:
    """
    Generates a random legal position of the Eternas game.

    Returns a list of 16 lists of 4 items each. Each item is 'g'
    (green bead), 'w' (white bead) or 0 (empty slot). Beads are put
    on a peg from the end of its list (index 3 is the first bead),
    so inside every peg list all 0s come before the beads.

    The position must be reachable in a real game:
    - at most 16 beads of each colour;
    - players move in turn, so the difference between the number of
      green and white beads is at most 1;
    - the game stops as soon as a winning combination appears, so a
      board may contain winning combinations only if they all share
      the bead placed by the very last move.

    Returns:
        list[list]: the generated board.

    Examples:
    >>> board = board_generation()
    >>> len(board)
    16
    >>> [len(peg) for peg in board] == [4] * 16
    True
    >>> [item for peg in board for item in peg if item not in (0, 'g', 'w')]
    []
    """

    board = [[0, 0, 0, 0] for _ in range(16)]
    next_level = [3 for _ in range(16)]

    first_color = choice(['g', 'w'])
    second_color = 'w' if first_color == 'g' else 'g'

    move_sequence = []

    for _ in range(16):
        move_sequence.append(first_color)
        move_sequence.append(second_color)

    for move in move_sequence:
        avaliable_pegs = [peg for peg in range(16) if next_level[peg] >= 0]

        peg = choice(avaliable_pegs)
        level = next_level[peg]

        board[peg][level] = move
        next_level[peg] -= 1

        if winning_combination(board):
            break

        # To create more random boards
        if randint(1, 25) == 25:
            break

    return board


def save_board(board: list[list], pathname: str):
    """
    Saves the board to a text file.

    Writes 16 lines, one per peg, in peg order. Each line holds the
    4 items of the peg list (level 0 to 3) separated by single
    spaces, e.g. "0 0 g w". The function returns nothing.

    Args:
        board (list[list]): 16 lists of 4 items ('g', 'w' or 0).
        pathname (str): path to the output file.

    Examples:
    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as out:
    ...     pass
    >>> board = [[0, 0, 0, 0] for _ in range(16)]
    >>> board[2] = [0, 0, 'g', 'w']
    >>> save_board(board, out.name)
    >>> with open(out.name, encoding='utf-8') as src:
    ...     lines = src.read().split('\\n')
    >>> lines[2]
    '0 0 g w'
    >>> lines[15]
    '0 0 0 0'
    >>> os.remove(out.name)
    """

    with open(pathname, 'w+', encoding='utf-8') as file:
        for peg in board:
            line = [' '.join(str(item) for item in peg)]
            file.write('\n'.join(line) + '\n')


def read_board(pathname: str) -> list[list]:
    """
    Reads a board from a text file written in the save_board format.

    The file holds 16 lines, one per peg; each line has the 4 items
    of the peg list (level 0 to 3) separated by spaces: 'g', 'w'
    or 0. Returns the board as a list of 16 lists of 4 items; empty
    slots are the integer 0, not the string '0'.

    Args:
        pathname (str): path to the input file.

    Returns:
        list[list]: the board read from the file.

    Examples:
    >>> import tempfile, os
    >>> content = '\\n'.join(['0 0 g w'] + ['0 0 0 0'] * 15)
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
    ...     _ = tmp.write(content)
    >>> board = read_board(tmp.name)
    >>> board[0]
    [0, 0, 'g', 'w']
    >>> board[1]
    [0, 0, 0, 0]
    >>> len(board)
    16
    >>> os.remove(tmp.name)
    """

    board = []

    with open(pathname, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace('\n', '')
            item = line.split()
            board.append([int(item[i]) if item[i].isdigit() else item[i] for i in range(4)])

    return board


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
