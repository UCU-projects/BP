"""
Модуль recursive_functions: рекурсивна побудова таблиці
та «розгортання» вкладених списків.
"""


def create_table(n: int, m: int) -> list[list[int]]:
    """
    Return a table with n rows and m columns (n, m >= 1).
    The first row and the first column are filled with 1,
    every other element is the sum of the element above it
    and the element to the left of it.
    The function must call itself.

    >>> create_table(1, 1)
    [[1]]
    >>> create_table(1, 3)
    [[1, 1, 1]]
    >>> create_table(3, 1)
    [[1], [1], [1]]
    >>> create_table(4, 6)
    [[1, 1, 1, 1, 1, 1], [1, 2, 3, 4, 5, 6], [1, 3, 6, 10, 15, 21], \
[1, 4, 10, 20, 35, 56]]
    """

    if n == 1:
        return [[1]*m]

    table = create_table(n-1, m)
    new_row = [1]

    for i in range(1, m):
        new_row.append(table[-1][i] + new_row[-1])

    table.append(new_row)

    return table


def flatten(lst):
    """
    Return a new list with all the elements of lst and of all the lists
    nested in it, in the same order. Empty nested lists disappear,
    all other elements (including 0, '', None, False, tuples) stay.
    If lst is not a list, return lst itself. lst must not change.
    The function must call itself.

    >>> flatten([1, [2]])
    [1, 2]
    >>> flatten([1, 2, [3, [4, 5], 6], 7])
    [1, 2, 3, 4, 5, 6, 7]
    >>> flatten(['wow', [2, [[]]], [True]])
    ['wow', 2, True]
    >>> flatten([])
    []
    >>> flatten([[]])
    []
    >>> flatten(3)
    3
    """

    if not isinstance(lst, list):
        return lst

    new_lst = []
    for el in lst:
        el = flatten(el)
        if isinstance(el, list):
            new_lst.extend(el)
        else:
            new_lst.append(el)

    return new_lst


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
