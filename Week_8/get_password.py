"""
Get password from a chain of files.
"""

def read_file(filename: str) -> tuple[str, int, str]:
    """
    Read a chained file and extract three logical blocks:
    a multi-line, space-padded password fragment, ordinal number and the next filename.

    The function tolerates arbitrary noise before the first '#' and after the
    last '#'.

    Parameters
    ----------
    filename : str
        Path to the file.

    Returns
    -------
    tuple[str, int, str]
        (raw_password_block, ordinal number, next_filename)

    Examples
    --------
    >>> simple_text = '#\\nA B\\n C\\n#\\n2\\n#\\nnext.txt\\n#'
    >>> print(simple_text)
    #
    A B
     C
    #
    2
    #
    next.txt
    #
    >>> import tempfile
    >>> with tempfile.NamedTemporaryFile(mode='r+', delete=False) as f:
    ...     _ = f.write(simple_text)
    >>> read_file(f.name)
    ('A B\\n C', 2, 'next.txt')

    >>> read_file('start.txt')
    ('A  A  N  C  Z\\n A  C  z  1\\n  A  3  a  l', 0, 'file1.txt')
    """

    with open(filename, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    password = ''
    order = 0
    next_file = ''
    noise_flag = False
    hash_in_file = data.count('#')
    hash_count = 0

    for line in data:
        if '#' in line or hash_in_file <= hash_count:
            hash_count += 1
            noise_flag = True
            continue

        if not noise_flag:
            continue

        if line.isdigit():
            order = int(line)
            continue

        if '.txt' in line or 'END' in line:
            next_file = line
            continue

        password += line + '\n'

    return (password[:-1], order, next_file)


def decode_raw_password(text: str) -> str:
    """
    Decodes a visually formatted "rail fence" block of text into a continuous string.
    The function reads characters column by column (top to bottom), ignoring spaces
    and blank lines. The height (number of rows) can be different.

    Parameters
    ----------
    text : str
        Multiline string where each line represents one "rail" or level
        of the encoded text. Spaces are used only for visual alignment.

    Returns
    -------
    str
        The decoded continuous string.

    Example:
    --------
    >>> decode_raw_password('A  A  N  C  Z\\n A  C  z  1\\n  A  3  a  l')
    'AAAAC3NzaC1lZ'
    >>> decode_raw_password('D  N  5  A  u\\n I  T  A  A\\n  1  E  A  I')
    'DI1NTE5AAAAIu'
    >>> decode_raw_password('p  n  6  x  w\\n T  V  e  4\\n  3  b  Z  Y')
    'pT3nVb6eZx4Yw'
    >>> decode_raw_password('A  1  x\\n b  2  y\\n  C  3 z')
    'AbC123xyz'
    >>> decode_raw_password('      t  W   \\n U      x     \\n  v      Q       ')
    'tUvWxQ'
    """

    data = text.split('\n')
    data_striped = []
    for line in data:
        new_line = ''
        for char in line:
            if char != ' ':
                new_line += char

        data_striped.append(new_line)

    password = ''
    max_ = max(len(line) for line in data_striped)
    for i in range(max_):
        for j, _ in enumerate(data_striped):
            try:
                if i < len(data_striped[j]) and data_striped[j][i] != ' ':
                    password += data_striped[j][i]
            except IndexError:
                continue

    return password


def collect_raw_passwords(startname: str) -> list[tuple[int, str, str]]:
    '''
    Traverse the entire chain of files starting from `startname`, decode each
    password fragment, and return a list of tuples containing the filename and its
    decoded fragment.

    Each tuple in the result represents one step in the chain:
        (ordinal number, current_filename, decoded_fragment)

    The traversal continues until a file specifies "END" as the next filename.

    Parameters
    ----------
    startname : str
        The name or path of the first file in the chain.

    Returns
    -------
    list[tuple[str, int, str]]
        A list of pairs, where:
          - the first element is the ordinal number of the fragment,
          - the second element is the filename processed,
          - the third element is the decoded part of the password.

    Examples
    --------
    >>> collect_raw_passwords('start.txt')
    [(0, 'start.txt', 'AAAAC3NzaC1lZ'), \
(1, 'file1.txt', 'DI1NTE5AAAAIu'), (3, 'file3.txt', 'Qx9vL2m5sK8rY'), \
(2, 'file2.txt', 'pT3nVb6eZx4Yw'), (4, 'end.txt', '7Hc2JqR5tUvWx')]
    '''
    result = []
    while True:
        raw_password, order, file = read_file(startname)
        password = decode_raw_password(raw_password)
        result.append((order, startname, password))
        if file == 'END':
            break

        startname = file

    return result


def write_password_file(raw_passwords: list[tuple[int, str, str]],
                       output_file: str) -> None:
    """
    Write all collected password fragments to a text file, followed by the
    final combined password according to the ordinal numbers.

    The file will contain:
      1. A header "Gathered fragments:".
      2. One line per fragment in the format "<ordinal number>,<filename>,<fragment>".
      3. A blank line with the label "Final password:".
      4. The complete password

    Parameters
    ----------
    raw_passwords : list[tuple[int, str, str]]
        List of tuples (ordinal number, filename, fragment), as returned by `collect_raw_passwords`.
    output_file : str
        Path to the destination file where the output will be written.

    Returns
    -------
    None

    Examples
    --------
    >>> raw_passwords = [(0, 'start.txt', 'AAAAC3NzaC1lZ'),\
(1, 'file1.txt', 'DI1NTE5AAAAIu'), (3, 'file3.txt', 'Qx9vL2m5sK8rY'),\
(2, 'file2.txt', 'pT3nVb6eZx4Yw'), (4, 'end.txt', '7Hc2JqR5tUvWx')]
    >>> write_password_file(raw_passwords, 'password.txt')
    >>> with open('password.txt', 'r', encoding='utf-8') as f:
    ...     print(f.read())
    Gathered fragments:
    0,start.txt,AAAAC3NzaC1lZ
    1,file1.txt,DI1NTE5AAAAIu
    3,file3.txt,Qx9vL2m5sK8rY
    2,file2.txt,pT3nVb6eZx4Yw
    4,end.txt,7Hc2JqR5tUvWx
    Final password:
    AAAAC3NzaC1lZDI1NTE5AAAAIupT3nVb6eZx4YwQx9vL2m5sK8rY7Hc2JqR5tUvWx
    """
    password = ''
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('Gathered fragments:\n')
        password = []
        for line in raw_passwords:
            password.append((line[0], line[2]))

        true_password = ''
        sorted_password = sorted(password)
        for part in sorted_password:
            true_password += part[1]

        for line in raw_passwords:
            file.write(str(line[0]) + ',' + line[1] + ',' + line[2] + '\n')

        file.write(f'Final password:\n{true_password}')


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
