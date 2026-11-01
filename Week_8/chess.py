"""
sdsds
"""

def read_board(filename: str) -> list:
    """
    Reads a chess board configuration from a file and returns it as a 2D list.
    Each line consists of 8 characters representing the pieces or empty squares.

    Piece Representation:
    - Uppercase letters represent white pieces.
    - Lowercase letters represent black pieces.
    - '.' represents an empty square.

    Piece Notation:
    - 'P' or 'p': Pawn
    - 'R' or 'r': Rook
    - 'N' or 'n': Knight
    - 'B' or 'b': Bishop
    - 'Q' or 'q': Queen
    - 'K' or 'k': King

    Coordinate System:
    - The board is an 8x8 grid.
    - The bottom-left corner (square 'a1') corresponds to coordinates (0, 0).
    - The top-right corner (square 'h8') corresponds to coordinates (7, 7).

    Parameters:
    -----------
    filename : str
        The path to the file containing the chess board configuration.

    Returns:
    --------
    list[list[str]]:
        A 2D list representing the chessboard, where each inner list is a row,
        and each element is a character representing a piece or an empty square.

    Example:
    --------
    >>> board = read_board("chess_board.txt")
    >>> board
    [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],\
 ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', 'P'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],\
 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    """
    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    board = []
    for line in data:
        board_line = []
        for item in line:
            board_line.append(item)

        board.insert(0, board_line)
    return board


def square_to_coordinate(square: str) -> tuple:
    """
    Converts a chess square notation to board coordinates.

    Parameters:
    -----------
    square : str
        The square in game board notation (e.g., 'e4').

    Returns:
    --------
    tuple[int, int]:
        A tuple (row_index, column_index) representing the position on the board.

    Example:
    --------
    >>> square_to_coordinate('a4')
    (3, 0)
    >>> square_to_coordinate('e5')
    (4, 4)
    """

    row, column = square

    y = ord(row) - ord('a')
    x = int(column) - 1

    return (x, y)

def get_move(board: list, move: tuple) -> tuple:
    """
    Calculates the result of moving a piece on the board without modifying the board.

    Parameters:
    -----------
    - board: list[list[str]]
        The current state of the chessboard.
    - move: tuple[str, str, int]
        The move to perform:
        - move[0]: str
            Starting square in chess board notation (e.g., 'e2').
        - move[1]: str
            Direction of movement ('U', 'D', 'L', 'R', 'UR', 'UL', 'DR', 'DL', 'N').
        - move[2]: int
            Number of steps to move (or specific code for knight moves).

    Returns:
    -----------
    - tuple[str, tuple[int, int], str]:
        - The figure to move.
        - The end coordinates as a tuple (row_index, column_index).
        - The piece at the destination square (captured piece), or
          '.' if empty, or '' if out of bounds.

    Directions:
    -----------
    - 'U': Up (increase row index).
    - 'D': Down (decrease row index).
    - 'L': Left (decrease column index).
    - 'R': Right (increase column index).
    - 'UR': Up-Right diagonal.
    - 'UL': Up-Left diagonal.
    - 'DR': Down-Right diagonal.
    - 'DL': Down-Left diagonal.
    - 'N': Knight moves, with move[2] specifying the move:
        1. Up 2, Left 1
        2. Up 1, Left 2
        3. Down 1, Left 2
        4. Down 2, Left 1
        5. Down 2, Right 1
        6. Down 1, Right 2
        7. Up 1, Right 2
        8. Up 2, Right 1

    Example:
    --------
    >>> board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],\
 ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', 'P'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],\
 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    >>> board[1][4]
    'P'
    >>> get_move(board, ("e2", "U", 2))
    ('P', (3, 4), '.')
    >>> get_move(board, ("e2", "D", 2))
    ('P', (-1, 4), '')
    >>> get_move(board, ("d8", "DR", 4))
    ('q', (3, 7), 'P')
    >>> get_move(board, ("g1", "N", 1))
    ('N', (2, 5), '.')
    """

    pos, mov, step = move

    pos = square_to_coordinate(pos)

    y, x = pos
    piece = board[y][x]
    # make list to make it shorter
    if mov == 'U':
        y += 1 * step
    elif mov == 'D':
        y -= 1 * step
    elif mov == 'L':
        x -= 1 * step
    elif mov == 'R':
        x += 1 * step
    elif mov == 'UR':
        y += 1 * step
        x += 1 * step
    elif mov == 'UL':
        y += 1 * step
        x -= 1 * step
    elif mov == 'DR':
        y -= 1 * step
        x += 1 * step
    elif mov == 'DL':
        y -= 1 * step
        x -= 1 * step
    elif mov == 'N':
        if step == 1:
            y += 1 * 2
            x -= 1 * 1
        elif step == 2:
            y += 1 * 1
            x -= 1 * 2
        elif step == 3:
            y += 1 * 2
            x += 1 * 1
        elif step == 4:
            y += 1 * 1
            x += 1 * 2
        elif step == 5:
            y -= 1 * 2
            x -= 1 * 1
        elif step == 6:
            y -= 1 * 2
            x -= 1 * 2
        elif step == 7:
            y -= 1 * 1
            x += 1 * 1
        elif step == 8:
            y -= 1 * 1
            x += 1 * 2


    if y < 0 or y >= 8 or x < 0 or x >= 8:
        return (piece, (y, x), '')

    return (piece, (y, x), board[y][x])


def make_move(board: list, move: tuple) -> list | None:
    """
    Attempts to make a move on the board, returning a new board if valid.

    Validity Conditions:
    --------
    - The starting square contains a piece (not empty).
    - The destination square is within the board boundaries.
    - The move results in capturing an opponent's piece or moving to an empty square.
    - Cannot capture a piece of the same color.

    Parameters:
    --------
    - board: list[list[str]]
        The current state of the chessboard.
    - move: tuple[str, str, int]
        The move to perform:
        - move[0]: str
            Starting square in algebraic notation (e.g., 'e2').
        - move[1]: str
            Direction of movement ('U', 'D', 'L', 'R', 'UR', 'UL', 'DR', 'DL', 'N').
        - move[2]: int
            Number of steps to move (or specific code for knight moves).

    Returns:
    --------
    - list[list[str]]:
        A new board with the move made if valid.
    - None:
        If the move is invalid.

    Notes:
    - Assumes pieces can move over other pieces without obstruction.

    Example:
    --------
    >>> board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],\
 ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', 'P'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],\
 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    >>> board[1][4]
    'P'
    >>> new_board = make_move(board, ("e2", "U", 2))
    >>> new_board[1][4]
    '.'
    >>> board[1][4]
    'P'
    >>> new_board[3][4]
    'P'
    >>> new_board = make_move(new_board, ("d8", "DR", 4))
    >>> new_board[7][3]
    '.'
    >>> new_board[3][7]
    'q'
    >>> new_board= make_move(board, ("g1", "N", 1))
    >>> board[0][6]
    'N'
    >>> board[2][5]
    '.'
    >>> new_board[2][5]
    'N'
    >>> new_board[0][6]
    '.'
    >>> new_board = make_move(board, ("e2", "D", 2))
    >>> new_board is None
    True
    """

    alg_coor, _, _= move
    piece, coor, square = get_move(board, move)
    y, x = coor

    if y < 0 or y >= 8 or x < 0 or x >= 8:
        return None

    if piece == '.':
        return None

    if square != '.' and ((piece.isupper() and square.isupper())
 or (piece.islower() and square.islower())):
        return None

    new_board = [row[:] for row in board]

    new_board[y][x] = piece
    orig_y, orig_x = square_to_coordinate(alg_coor)
    new_board[orig_y][orig_x] = '.'

    return new_board


def play_game(board: list, moves: list) -> list:
    """
    Plays a sequence of moves on the board, ignoring invalid moves.

    Parameters:
    --------
    - board: list[list[str]]
        The initial state of the chessboard.
    - moves: list[str]
        A list of moves in string format.
        Each move is formatted as "square direction steps",
        e.g., "e2 U 2" moves the piece at 'e2' two steps up.

    Returns:
    --------
    - list[list[str]]:
        The resulting board after applying all valid moves.

    Notes:
    --------
    - Invalid moves are ignored; the board remains unchanged for those moves.
    - Does not enforce detailed chess rules (e.g., check, checkmate).

    Example:
    --------
    >>> board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],\
 ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', 'P'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],\
 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    >>> moves = ['e2 U 2', 'e1 D 2', 'e7 D 2', 'e1 U 1', 'e8 D 1']
    >>> new_board = play_game(board, moves)
    >>> new_board[3][4]
    'P'
    >>> new_board[4][4]
    'p'
    >>> new_board[1][4]
    'K'
    >>> new_board[6][4]
    'k'
    """

    for move in moves:
        alg_coor, mov, step = move.split()
        move = (alg_coor, mov, int(step))

        new_board = make_move(board, move)
        if new_board is None:
            continue

        board = new_board

    return board


def save_board(board: list, filename: str) -> None:
    """
    Saves the board to a file in the same format used by `read_board`.

    Parameters:
    --------
    - board: list[list[str]]
        The chessboard to save.
    - filename: str
        The path to the file where the board will be saved.

    Returns:
    --------
    - None

    Notes:
    --------
    - The board is written from top (rank 8) to bottom (rank 1).
    - Each row is written as a string of 8 characters.

    Example:
    --------
    >>> board = [['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],\
 ['P', 'P', 'P', 'P', 'P', 'P', 'P', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', 'P'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['.', '.', '.', '.', '.', '.', '.', '.'],\
 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],\
 ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']]
    >>> moves = ['e2 U 2', 'e7 D 2', 'e1 U 1', 'e8 D 1']
    >>> new_board = play_game(board, moves)
    >>> save_board(new_board, 'result.txt')
    >>> with open('result.txt', 'r', encoding='utf-8') as file:
    ...    print(file.read())
    rnbq.bnr
    ppppkppp
    ........
    ....p...
    ....P..P
    ........
    PPPPKPP.
    RNBQ.BNR
    """

    with open(filename, 'w', encoding='utf-8') as file:
        line = ''
        for i in range(1, 9):
            line += ''.join(board[-i]) +'\n'

        file.write(line[:-1])


if __name__=='__main__':
    import doctest
    print(doctest.testmod())
