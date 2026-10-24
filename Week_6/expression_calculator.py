"""
Lab work 6
String calculator
"""


def calculate_expression(expression: str) -> int | str:
    """
    Calculate expression just like calculator but string(only ukrainian)
    Supports only addition, multiplication, substracting, division
    Doesn't support right order of math operations

    :param expression: str, A string which contains math expression and starts with "Cкільки буде"
    :return: int | str, A result of the equation, 
    if syntax incorrect or operation doesn't supports, then 'Неправильний вираз!' 

    >>> calculate_expression('Скільки буде 8 відняти 3?')
    5
    >>> calculate_expression('Скільки буде 7 додати 3 помножити на 5?')
    50
    >>> calculate_expression('Скільки буде 10 поділити на -2 додати 11 мінус -3?')
    9
    >>> calculate_expression('Скільки буде 3 в кубі?')
    'Неправильний вираз!'
    >>> calculate_expression('Скільки буде 10 поділити на -2 додати 11 мінус -3 поділити на 0?')
    'Неправильний вираз!'
    >>> calculate_expression('Скільки буде 10 поділити на -2 додати 11 мінус -3 помножити на 0?')
    0
    >>> calculate_expression('Скільки буде 10 поділити на -2?')
    -5
    >>> calculate_expression('Скільки буде 3 поділити на 2?')
    1
    >>> calculate_expression('Скільки буде 3 поділити на 2')
    'Неправильний вираз!'
    >>> calculate_expression('3 плюс 2?')
    'Неправильний вираз!'
    """

    if not (expression.startswith('Скільки буде') and expression.endswith('?')):
        return 'Неправильний вираз!'

    # Ensure there is no unparsable chars
    body = expression[len('Скільки буде'):-1].strip()

    # List of tuples
    operations = [
        ('додати', '+'),
        ('плюс', '+'),
        ('відняти', '-'),
        ('мінус', '-'),
        ("помножити на", "*"),
        ("поділити на", "/"),
    ]

    # Doing this because want to use split(), so "*", "/" won't parse correctly
    for exp, op in operations:
        body = body.replace(exp, op)

    # Dividing operations and numbers into pieces for convinience
    body = body.split()

    try:
        value = int(body[0])
    except ValueError:
        return 'Неправильний вираз!'

    i = 1
    while i < len(body):

        symbol = body[i]

        # Syntax checks
        # Starting with operation, so if not then syntax wrong,
        # if syntax right, then there must be something
        if symbol not in ('+', '-', '*', '/') or i + 1 >= len(body):
            return 'Неправильний вираз!'

        # If syntax right, then next symbol is number
        try:
            num = int(body[i + 1])
        except ValueError:
            return 'Неправильний вираз!'

        if symbol == '+':
            value += num
        elif symbol == '-':
            value -= num
        elif symbol == '*':
            value *= num
        elif symbol == '/':
            if num == 0:
                return 'Неправильний вираз!'

            # Floor division in order to not use int later
            value //= num

        # Two chars at once processing
        i += 2

    return value


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
