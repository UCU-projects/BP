"""
Calculus: maximal values, limits, derivatives, tangents and roots.
"""


def find_max_value(func: callable, points: list[float]) -> float:
    """Find the maximal value of a function at given points.

    Args:
        func (callable): The function to evaluate.
        points (list[float]): A list of points at which to evaluate the function.

    Returns:
        float: The maximal value of the function at the given points
               rounded to 2 decimal places.

    Examples:

    >>> find_max_value(lambda x: x ** 2 + x, [1, 2, 3, -1])
    12
    >>> find_max_value(lambda x: x + 1/2 + x, [1, 2, 3, -1])
    6.5
    """
    return round(max((func(x)) for x in points), 2)


def find_max_points(func: callable, points: list[float]) -> set[float]:
    """Find the points where the function has the maximal value.

    Compare the exact (not rounded) values of the function.

    Args:
        func (callable): The function to evaluate.
        points (list[float]): A list of points at which to evaluate the function.

    Returns:
        set[float]: A set of points where the function has the maximal value.

    Examples:
    >>> find_max_points(lambda x: x ** 2 + x, [1, 2, 3, -1])
    {3}
    >>> find_max_points(lambda x: -x ** 2 + 4*x, [1, 0, 3, -1])
    {1, 3}
    >>> find_max_points(lambda x: x ** 2, [1, 0, 3, float('inf')])
    {inf}
    """


    max_value = func(points[0])
    max_points = set()

    for x in points:
        value = func(x)
        if value > max_value:
            max_points.clear()
            max_value = value
            max_points.add(x)
        elif value == max_value:
            max_points.add(x)

    return max_points


def compute_limit(seq: callable) -> float:
    """Compute the limit of a convergent sequence.

    Args:
        seq (callable): A function representing the sequence.

    Returns:
        float: The limit of the sequence rounded to 2 decimal places.

    Examples:
        >>> compute_limit(lambda n: (n ** 2 + n) / (3*n ** 2))
        0.33
        >>> compute_limit(lambda n: (n / n))
        1.0
        
    """

    n = 1
    tol = 1e-3

    while abs(seq(n) - seq(n * 10)) > tol:
        n *= 10

    return round(seq(n), 2)


def compute_derivative(func: callable, x_0: float) -> float:
    """Compute the derivative of a function at a given point.

    Args:
        func (callable): The function to differentiate.
        x_0 (float): The point at which to compute the derivative.

    Returns:
        float: The derivative of the function at the given point
               rounded to 2 decimal places.

    Examples:
        >>> compute_derivative(lambda x: x ** 2 + x, 2)
        5.0
        >>> compute_derivative(lambda x: 5, 2)
        0.0
    """

    delta_x = 1
    tol = 1e-3
    while abs(((func(x_0 + delta_x*10) - func(x_0)) / (delta_x*10)) -
        (func(x_0 + delta_x) - func(x_0)) / delta_x) > tol:

        delta_x /= 10

    return round((func(x_0 + delta_x) - func(x_0)) / delta_x, 2)


def get_tangent(func: callable, x_0: float) -> str:
    """Calculate the equation of the tangent line to a given function at a specified point.

    This function computes the tangent line to the input function `func` at the point `x_0`.
    The tangent line is represented in the form of a linear equation.

    Args:
        func (callable): A function for which the tangent line is to be calculated.
        x_0 (float): The x-coordinate at which the tangent line is computed.

    Returns:
        str: A string representing the equation of the tangent line y = a * x + b
             in the format 'a * x + b', where 'a' is the slope and 'b' is the y-intercept,
             both rounded to 2 decimal places (see the examples for a = 0, b = 0,
             a = 1 and a = -1).

    Examples:
    >>> import math
    >>> get_tangent(lambda x: 1 / x, 2)
    '- 0.25 * x + 1.0'
    >>> get_tangent(math.sin, 1)
    '0.54 * x + 0.3'
    >>> get_tangent(lambda x: x ** 2 + x, 2)
    '5.0 * x - 4.0'
    >>> get_tangent(lambda x: - x ** 2 + x, 2)
    '- 3.0 * x + 4.0'
    >>> get_tangent(lambda x: x, 2)
    'x'
    >>> get_tangent(lambda x: -x, 2)
    '- x'
    >>> get_tangent(lambda x: x**2-2, 0.5)
    'x - 2.25'
    >>> get_tangent(lambda x: -x**2-2, 0.5)
    '- x - 1.75'
    """
    k = compute_derivative(func, x_0)
    b = round(k * -x_0 + func(x_0), 2)

    if k == 0:
        return f"- {abs(b)}" if b < 0 else f"{b}"

    if k == 1:
        k =  'x'
    elif k == -1:
        k = '- x'
    elif k > 0:
        k = f'{k} * x'
    else:
        k = f'- {abs(k)} * x'

    if b == 0:
        return k
    if b > 0:
        return f"{k} + {b}"

    return f"{k} - {abs(b)}"


def get_root(func: callable, a: float, b: float) -> float:
    """Compute the root of a function in a given interval.

    The function takes values of different signs at a and b
    and has exactly one root in the interval.

    Args:
        func (callable): The function to evaluate.
        a (float): The start of the interval.
        b (float): The end of the interval.

    Returns:
        float: The root of the function in the interval rounded to 2 decimal places.

    Examples:
    >>> get_root(lambda x: x - 1, 0, 3)
    1.0
    >>> get_root(lambda x: x ** 2 - 2, 0, 2)
    1.41
    >>> get_root(lambda x: x, -3095454545403494, 3945454545450954)
    0.0

    """
    tol = 1e-2
    while b - a > tol:
        mid_point = (a + b) / 2
        if func(mid_point) == 0:
            break

        if func(a) * func(mid_point) < 0:
            b = mid_point
        else:
            a = mid_point

    return round(mid_point, 2)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
