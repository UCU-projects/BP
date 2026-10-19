"""
Complete all of the following functions. Currently, they all just
'pass' rather than explicitly return value, meaning they
implicitly return None. They all include doctests, which you can
test by running this file.
The doctests are just examples. Feel free to add your doctests.
"""


# ****************************************
# Problem 1
# ****************************************
def count_sheep(n: int) -> str | None:
    """
    Generate a string that counts sheep from 1 to n.

    This function creates a string for counting sheep to help fall asleep.
    For a given non-negative integer n, it returns a string in the format:
    "1 sheep...2 sheep...3 sheep...". Each number is followed by " sheep..."

    If the argument is not a non-negative integer, the function should return None.

    :param n: int, A non-negative integer representing how many sheep to count.
    :return: str or None, The sheep counting string, or None if input is invalid.

    >>> count_sheep(0)
    ''
    >>> count_sheep(1)
    '1 sheep...'
    >>> count_sheep(2)
    '1 sheep...2 sheep...'
    >>> count_sheep(3)
    '1 sheep...2 sheep...3 sheep...'
    >>> count_sheep(-5)
    >>> count_sheep(2.4)
    >>> count_sheep('sddsjdk')
    >>> count_sheep(True)
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        return None

    string = ''

    if n > 0:
        for i in range(1, n+1):
            string += str(i) + ' sheep...'
        return string

    return string


# ****************************************
# Problem 2
# ****************************************
def remove_vowels(text: str) -> str | None:
    """
    Remove all vowels from the given string and return the modified string.

    This function removes all vowel characters (a, e, i, o, u, A, E, I, O, U)
    from the input string while preserving all other characters including
    whitespace, punctuation, and the letter 'y'.

    If the argument is not a string, the function should return None.

    :param text: str, The input string from which vowels should be removed.
    :return: str or None, The string without vowels, or None if input is invalid.

    >>> remove_vowels("Hello World!")
    'Hll Wrld!'
    >>> remove_vowels("xyz")
    'xyz'
    >>> remove_vowels("AEIOU")
    ''
    >>> remove_vowels(123) is None
    True
    >>> remove_vowels('"@7438764')
    '"@7438764'
    >>> remove_vowels("")
    ''
    """
    if not isinstance(text, str):
        return None

    string = ''

    for char in text:
        if char in ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'):
            continue

        string += char

    return string


# ****************************************
# Problem 3
# ****************************************
def round_to_next_five(n: int) -> int | None:
    """
    Round the given integer to the next (greater than or equal) multiple of 5.

    This function takes an integer and returns the smallest multiple of 5
    that is greater than or equal to the input number. If the input is
    already a multiple of 5, it returns the input unchanged.

    If the argument is not an integer, the function should return None.

    :param n: int, The integer to be rounded.
    :return: int or None, The next multiple of 5, or None if input is invalid.

    >>> round_to_next_five(2)
    5
    >>> round_to_next_five(30)
    30
    >>> round_to_next_five(-2)
    0
    >>> round_to_next_five(3.5) is None
    True
    >>> round_to_next_five(120023)
    120025
    >>> round_to_next_five(0)
    0
    >>> round_to_next_five(6)
    10
    >>> round_to_next_five(-10)
    -10
    >>> round_to_next_five(True)
    """
    if not isinstance(n, int) or isinstance(n, bool):
        return None

    remainder = n % 5

    if remainder == 0:
        return n

    n += 5 - remainder
    return n


# ****************************************
# Problem 4
# ****************************************
def hex_char_to_int(c: str) -> int | None:
    """
    Convert a single hexadecimal character to its integer value (0-15).

    This function takes a single character representing a hexadecimal digit
    (0-9, A-F, a-f) and returns its corresponding integer value from 0 to 15.
    If the character is not a valid hexadecimal digit, the function returns -1.

    This is a helper function useful for parsing hexadecimal color codes.

    If the argument is not a single character string, the function should return None.

    :param c: str, A single character to convert (must be one character long).
    :return: int or None, Integer value 0-15 for valid hex digits, -1 for invalid
                          hex characters, or None if input is invalid.

    >>> hex_char_to_int('0')
    0
    >>> hex_char_to_int('A')
    10
    >>> hex_char_to_int('a')
    10
    >>> hex_char_to_int('#')
    -1
    >>> hex_char_to_int('AB')
    >>> hex_char_to_int('F')
    15
    >>> hex_char_to_int('G')
    -1
    >>> hex_char_to_int(' ')
    -1
    """

    if not isinstance(c, str):
        return None

    i = 0
    for _ in c:
        i += 1

    if i != 1:
        return None

    ord_c = ord(c)
    if c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
        return int(c)

    if ord('A') <= ord_c <= ord('F'):
        return 10 + ord_c - ord('A')

    if ord('a') <= ord(c) <= ord('f'):
        return 10 + ord_c - ord('a')

    return -1


# ****************************************
# Problem 5
# ****************************************
def rot13(message: str) -> str | None:
    """
    Encode a string using the ROT13 cipher.

    ROT13 is a simple letter substitution cipher that replaces each letter
    with the letter 13 positions after it in the alphabet. It's a special
    case of the Caesar cipher. Since there are 26 letters in the alphabet,
    applying ROT13 twice returns the original text.

    Only letters (A-Z, a-z) are shifted. Numbers, spaces, punctuation, and
    special characters remain unchanged. Case is preserved.

    If the argument is not a string, the function should return None.

    :param message: str, The message to encode with ROT13.
    :return: str or None, The ROT13-encoded message, or None if input is invalid.

    >>> rot13("test")
    'grfg'
    >>> rot13("Hello, World!")
    'Uryyb, Jbeyq!'
    >>> rot13("Why did the chicken cross the road?")
    'Jul qvq gur puvpxra pebff gur ebnq?'
    >>> rot13('Jul qvq gur puvpxra pebff gur ebnq?')
    'Why did the chicken cross the road?'
    >>> rot13("123!@# ")
    '123!@# '
    >>> rot13("aBc XyZ")
    'nOp KlM'
    >>> rot13(123)
    >>> rot13("Python 3.10!")
    'Clguba 3.10!'
    """

    if not isinstance(message, str):
        return None

    string = ''

    for char in message:
        if not ('A' <= char <= 'Z' or 'a' <= char <= 'z'):
            string += char
            continue

        if 'A' <= char <= 'Z':
            # Subtracting 'A' in order to have number in alphabet interval then shifting it by 13
            # Using modulo to know position if shifting gone over alphabet
            # Then returning it to letter positions
            string += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
        elif 'a' <= char <= 'z':
            string += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))

    return string


# ****************************************
# Problem 6
# ****************************************
def square_digits(n: int) -> int | None:
    """
    Square every digit of a number and concatenate them into a new integer.

    This function takes an integer, squares each of its digits individually,
    and concatenates the results to form a new integer. For example, the number
    9119 becomes 811181 because 9²=81, 1²=1, 1²=1, 9²=81.

    If the argument is not an integer, the function should return None.
    For negative numbers, the sign is ignored and only digits are processed.

    :param n: int, The integer whose digits should be squared.
    :return: int or None, The new integer formed by concatenating squared digits,
                          or None if input is invalid.

    >>> square_digits(9119)
    811181
    >>> square_digits(0)
    0
    >>> square_digits(5)
    25
    >>> square_digits(3.5)
    >>> square_digits(-1232)
    1494
    >>> square_digits('123')
    >>> square_digits(22)
    44
    >>> square_digits(True)
    """

    if not isinstance(n, int) or isinstance(n, bool):
        return None

    string = ''
    n = str(n)

    for num in n:
        if '0' <= num <= '9':
            string += str(int(num) ** 2)

    return int(string)


# ****************************************
# Problem 7
# ****************************************
def multiply_until_single_digit(num: int) -> int | None:
    """
    Calculate the multiplicative persistence of a positive integer.

    Multiplicative persistence is the number of times you must multiply
    the digits of a number until you reach a single digit. For example,
    39 has persistence 3 because: 3*9=27, 2*7=14, 1*4=4 (3 steps).

    If the argument is not a non-negative integer, the function should return None.

    :param num: int, A non-negative integer to calculate persistence for.
    :return: int or None, The multiplicative persistence, or None if input is invalid.

    >>> multiply_until_single_digit(39)
    3
    >>> multiply_until_single_digit(999)
    4
    >>> multiply_until_single_digit(4)
    0
    >>> multiply_until_single_digit(-5)
    >>> multiply_until_single_digit('aaasa')
    >>> multiply_until_single_digit(True)
    """

    if not isinstance(num, int) or isinstance(num, bool) or num < 0:
        return None

    num = str(num)

    i = 0
    while len(num) != 1:
        i += 1
        output = 1
        for n in num:
            n = int(n)
            output *= n
        num = str(output)

    return i


# ****************************************
# Problem 8
# ****************************************
def find_n_cubes(m: int) -> int | None:
    """
    Find the number of cubes needed to build a pile with a given total volume.

    This function determines how many cubes are needed to construct a building
    where each cube has a volume that follows the pattern: n³ + (n-1)³ + (n-2)³ + ... + 1³.
    The bottom cube has volume n³, the one above it has volume (n-1)³, and so on
    until the top cube with volume 1³.

    Given the total volume m, the function returns the number n of cubes needed,
    or -1 if no such n exists.

    If the argument is not a positive integer, the function should return None.

    :param m: int, The total volume of the building (must be positive).
    :return: int or None, The number of cubes n, -1 if impossible, or None if input is invalid.

    >>> find_n_cubes(1)
    1
    >>> find_n_cubes(36)
    3
    >>> find_n_cubes(4)
    -1
    >>> find_n_cubes(0)
    >>> find_n_cubes('sddsd')
    >>> find_n_cubes(2.1)
    >>> find_n_cubes(True)
    """

    if not isinstance(m, int) or isinstance(m, bool) or m <= 0:
        return None

    n = 0
    while m > 0:
        n += 1
        m -= n ** 3

    if m == 0:
        return n

    return -1


# ****************************************
# Problem 9
# ****************************************
def count_carries(num1:int, num2:int) -> int | None:
    """
    Count the number of carry operations when adding two numbers.

    A carry operation occurs during addition when the sum of digits in a column
    is 10 or greater, requiring a digit to be transferred to the next column.
    For example, adding 123 + 456: 3+6=9 (no carry), 2+5=7 (no carry), 1+4=5 (no carry).
    But adding 123 + 594: 3+4=7 (no carry), 2+9=11 (1 carry), 1+5+1(carry)=7 (no carry).

    Both numbers should be non-negative integers. The function handles numbers
    of different lengths by zero-padding the shorter one.

    If either argument is not a non-negative integer, the function should return None.

    :param num1: int, The first non-negative integer.
    :param num2: int, The second non-negative integer.
    :return: int or None, The number of carry operations, or None if input is invalid.

    >>> count_carries(123, 456)
    0
    >>> count_carries(555, 555)
    3
    >>> count_carries(9, 99)
    2
    >>> count_carries(1, 9)
    1
    >>> count_carries(-5, 10)
    >>> count_carries('sdhsdh', 2)
    >>> count_carries(999, 1)
    3
    >>> count_carries(0, 0)
    0
    >>> count_carries(True, 999)
    """
    if (not (isinstance(num1, int) and isinstance(num2, int)) or
        isinstance(num1, bool) or isinstance(num2, bool) or
        min(num1, num2) < 0):

        return None

    carry = 0
    plus_one = 0

    while num1 > 0 or num2 > 0:
        # Finding last digit
        dig1 = num1 % 10
        dig2 = num2 % 10
        total = plus_one + dig1 + dig2

        if total >= 10:
            carry += 1
            plus_one = 1
        else:
            plus_one = 0

        # Removing digit we already worked with
        num1 //= 10
        num2 //= 10

    return carry


# ****************************************
# Problem 10
# ****************************************
def collatz_length(n: int) -> int | None:
    """
    Calculate the length of the Collatz sequence for a given positive integer.

    The Collatz Conjecture states that for any positive natural number n,
    this process:
    - If n is even: divide it by 2
    - If n is odd: multiply it by 3 and add 1
    - Continue until n reaches 1
    will eventually reach n = 1.

    This function returns the number of steps required
    to reach 1, including the initial number and the final 1.

    If the argument is not a positive integer, the function should return None.

    :param n: int, A positive integer to calculate the Collatz sequence length for.
    :return: int or None, The length of the Collatz sequence, or None if input is invalid.

    >>> collatz_length(1)
    1
    >>> collatz_length(2)
    2
    >>> collatz_length(3)
    8
    >>> collatz_length(20)
    8
    >>> collatz_length(0)
    >>> collatz_length('sdhjs')
    >>> collatz_length(5)
    6
    >>> collatz_length(True)
    """
    if not isinstance(n, int) or isinstance(n, bool) or n <= 0:
        return None

    length = 1
    while n != 1:
        length += 1
        if n % 2 == 0:
            n //= 2
        else:
            n = n * 3 + 1

    return length


# ****************************************
# Problem 11
# ****************************************
def hex_to_rgb(hex_color: str) -> str | None:
    """
    Extract the individual RGB (Red, Green, Blue) component values from a hex color.

    This function accepts a hexadecimal color string (case-insensitive) in the
    format "#RRGGBB" and returns a string representation of the RGB values
    in the format "r: R, g: G, b: B" where R, G, and B are integers from 0 to 255.

    The function does not support shorthand hexadecimal notation (e.g., "#FFF").
    You may use the hex_char_to_int() function from Problem 4 to help with conversion.
    For example, for "#FF9933":
    - red is 'FF', that corresponds hex_char_to_int('F')*16+hex_char_to_int('F')
    - green is '99', that corresponds hex_char_to_int('9')*16+hex_char_to_int('9')
    - blue is '33', that corresponds hex_char_to_int('3')*16+hex_char_to_int('3')

    If the argument is not a valid hex color string, the function should return None.

    :param hex_color: str, A hexadecimal color string in format "#RRGGBB".
    :return: str or None, RGB values as "r: R, g: G, b: B", or None if input is invalid.

    >>> hex_to_rgb("#FF9933")
    'r: 255, g: 153, b: 51'
    >>> hex_to_rgb("#000000")
    'r: 0, g: 0, b: 0'
    >>> hex_to_rgb("#AbCdEf")
    'r: 171, g: 205, b: 239'
    >>> hex_to_rgb("#FFF")
    >>> hex_to_rgb('000000')
    >>> hex_to_rgb(000000)
    >>> hex_to_rgb('#FF22GG')
    >>> hex_to_rgb("#ffffff")
    'r: 255, g: 255, b: 255'
    """
    if not isinstance(hex_color, str) or len(hex_color) != 7:
        return None

    hash_, red1, red2, green1, green2, blue1, blue2 = hex_color

    if hash_ != '#':
        return None

    red1 = hex_char_to_int(red1)
    red2 = hex_char_to_int(red2)
    green1 = hex_char_to_int(green1)
    green2 = hex_char_to_int(green2)
    blue1 = hex_char_to_int(blue1)
    blue2 = hex_char_to_int(blue2)

    if min(red1, red2, green1, green2, blue1, blue2) < 0:
        return None

    r_value = red1*16 + red2
    g_value = green1*16 + green2
    b_value = blue1*16 + blue2

    return f'r: {r_value}, g: {g_value}, b: {b_value}'


# ****************************************
# Problem 12
# ****************************************
def is_valid_isbn10(isbn: str) -> bool | None:
    """
    Validate an ISBN-10 identifier.

    An ISBN-10 is a 10-character string where the first 9 characters are digits (0-9)
    and the last character can be a digit or 'X' (representing 10).

    An ISBN-10 is valid if the sum of each digit multiplied by its position
    (1-indexed) modulo 11 equals zero:
    (d1*1 + d2*2 + d3*3 + ... + d10*10) % 11 = 0

    If the argument is not a string of exactly 10 characters, the function
    should return None.

    :param isbn: str, A string representing an ISBN-10 identifier.
    :return: bool or None, True if valid ISBN-10, False if invalid format but
                           correct length, or None if input is invalid.

    >>> is_valid_isbn10("1112223339")
    True
    >>> is_valid_isbn10("1112223330")
    False
    >>> is_valid_isbn10("1112223339X")
    >>> is_valid_isbn10(1112223339)
    """

    if not isinstance(isbn, str) or len(isbn) != 10:
        return None

    sum_ = 0

    i = 0
    for char in isbn:
        i += 1
        try:
            char = int(char)
        except ValueError:
            if char != 'X' and i != 10:
                return None
            char = 10
        sum_ += char * i

    return sum_ % 11 == 0



# ****************************************
# Problem 13
# ****************************************
def prime_factors(n: int) -> str | None:
    """
    Find the prime factor decomposition of a positive integer n > 1.

    This function returns a string representation of the prime factorization
    in the form "(p1**n1)(p2**n2)...(pk**nk)" where pi are prime factors in
    increasing order and ni are their exponents. If an exponent is 1, it is
    omitted from the output.

    For example: 86240 = 2^5 * 5^1 * 7^2 * 11^1 returns "(2**5)(5)(7**2)(11)"

    If the argument is not an integer greater than 1, the function should return None.

    :param n: int, A positive integer greater than 1.
    :return: str or None, Prime factorization string, or None if input is invalid.

    >>> prime_factors(86240)
    '(2**5)(5)(7**2)(11)'
    >>> prime_factors(2)
    '(2)'
    >>> prime_factors(4)
    '(2**2)'
    >>> prime_factors(100)
    '(2**2)(5**2)'
    >>> prime_factors(7775460)
    '(2**2)(3**3)(5)(7)(11**2)(17)'
    >>> prime_factors(1)
    >>> prime_factors(0)
    >>> prime_factors(True)
    >>> prime_factors(479001599)
    '(479001599)'
    """

    if not isinstance(n, int) or n <= 1:
        return None

    string = ''

    # Smallest prime
    num = 2
    while num * num <= n:
        if n % num == 0:
            exp = 0
            while n % num == 0:
                exp += 1
                # Just division turns into float, so using ground version
                n //= num
            if exp == 1:
                string += f'({num})'
                continue
            string += f'({num}**{exp})'
        num += 1

    if n > 1:
        string += f'({n})'

    return string


# ****************************************
# Problem 14
# ****************************************
def reduce_fraction(numerator, denominator):
    """
    Reduce a fraction to its simplest form and return it as a string.

    Don't use recursion! Investigate the Euclidean algorithm.
    This function takes a numerator and denominator as positive integers
    and returns the fraction reduced to its lowest terms in the format
    'numerator/denominator'. The function finds the greatest common divisor
    (GCD) of both numbers and divides them by it.

    If either argument is not a positive integer, the function should return None.

    :param numerator: int, The numerator of the fraction (must be positive).
    :param denominator: int, The denominator of the fraction (must be positive).
    :return: str or None, The reduced fraction as a string, or None if input is invalid.

    >>> reduce_fraction(45, 120)
    '3/8'
    >>> reduce_fraction(10, 5)
    '2/1'
    >>> reduce_fraction(7, 13)
    '7/13'
    >>> reduce_fraction(5, 0)
    >>> reduce_fraction(True, 13)
    """
    if (not (isinstance(numerator, int) and isinstance(denominator, int)) or
        isinstance(numerator, bool) or isinstance(denominator, bool) or
        min(numerator, denominator) <= 0):

        return None

    min_num = min(numerator, denominator)
    max_num = max(numerator, denominator)

    # Using euclidian algotrithm
    # Because I can know remainder with "%", I can just do permutation without extra steps
    while min_num != 0:
        max_num, min_num = min_num, max_num % min_num

    return f'{numerator//max_num}/{denominator//max_num}'


# ****************************************
# Problem 15
# ****************************************
def to_binary(n: int) -> str | None:
    """
    Convert a non-negative integer to its binary representation as a string.

    This function converts a decimal number to binary without using
    the built-in bin() function. The result contains no '0b' prefix
    and no leading zeros.

    If the argument is not a non-negative integer, the function should return None.

    :param n: int, A non-negative integer to convert.
    :return: str or None, The binary representation, or None if input is invalid.

    >>> to_binary(0)
    '0'
    >>> to_binary(1)
    '1'
    >>> to_binary(5)
    '101'
    >>> to_binary(64)
    '1000000'
    >>> to_binary(255)
    '11111111'
    >>> to_binary(-3)
    >>> to_binary(2.5)
    >>> to_binary(5039)
    '1001110101111'
    >>> to_binary(2)
    '10'
    """

    if not isinstance(n, int) or n < 0:
        return None

    exp = 0
    while n >= 2**(exp+1):
        exp += 1

    string = ''
    while n >= 0 and exp != -1:
        if n - 2**exp >= 0:
            n -= 2**exp
            string += '1'
        else:
            string += '0'
        exp -= 1

    return string


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
