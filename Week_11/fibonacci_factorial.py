"""
Модуль fibonacci_factorial: факторіал і числа Фібоначчі
рекурсивно та ітеративно, порівняння часу виконання.
"""
import time


def factorial_recursive(n: int) -> int:
    """
    Return n! for a non-negative integer n. Works recursively.

    >>> factorial_recursive(0)
    1
    >>> factorial_recursive(3)
    6
    >>> factorial_recursive(7)
    5040
    """
    fibonacci_recursive.iterations += 1
    if n <= 1:
        return 1

    return n * factorial_recursive(n-1)

factorial_recursive.iterations = 0


def factorial_iterative(n: int) -> int:
    """
    Return n! for a non-negative integer n. Works iteratively.

    >>> factorial_iterative(0)
    1
    >>> factorial_iterative(3)
    6
    >>> factorial_iterative(7)
    5040
    """
    factorial = 1

    for i in range(1, n+1):
        factorial_iterative.iterations += 1
        factorial *= i

    return factorial

factorial_iterative.iterations = 0


def fibonacci_recursive(n: int) -> int:
    """
    Return the n-th Fibonacci number (the sequence 1, 1, 2, 3, 5, ...,
    indices start from 0). Works recursively.

    >>> fibonacci_recursive(0)
    1
    >>> fibonacci_recursive(1)
    1
    >>> fibonacci_recursive(5)
    8
    >>> fibonacci_recursive(9)
    55
    """
    fibonacci_recursive.iterations += 1

    if n <= 1:
        return 1
    return fibonacci_recursive(n-1) + fibonacci_recursive(n-2)

fibonacci_recursive.iterations = 0


def fibonacci_iterative(n: int) -> int:
    """
    Return the n-th Fibonacci number (the sequence 1, 1, 2, 3, 5, ...,
    indices start from 0). Works iteratively.

    >>> fibonacci_iterative(0)
    1
    >>> fibonacci_iterative(1)
    1
    >>> fibonacci_iterative(5)
    8
    >>> fibonacci_iterative(50)
    20365011074
    """
    prev, curr = 1, 1
    for _ in range(2, n + 1):
        fibonacci_iterative.iterations += 1
        prev, curr = curr, prev + curr
    return curr

fibonacci_iterative.iterations = 0


def time_test(function: callable, n: int, verbose: bool = False) -> float:
    """
    Run function(n) and return the time it took in seconds.
    If verbose is True, also print additional information
    (what exactly, you decide yourself).
    """

    start = time.perf_counter()
    function(n)
    end = time.perf_counter()

    elapsed = end - start

    if verbose:
        print(f'Iterations: {function.iterations}')

    return f'{elapsed:.0f} second(s) elapsed'

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
    print(time_test(fibonacci_iterative, 220000, True))
