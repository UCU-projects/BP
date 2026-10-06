''' Program for calculating one solution for cubic '''
from math import cbrt
a = float(input("Enter first coefficient: "))
b = float(input("Enter second coefficient: "))
c = float(input("Enter third coefficient: "))
d = float(input("Enter fourth coefficient: "))

# Optimizing formula because of repeated parts
first_part = - (b ** 3 / (27 * a ** 3)) + ((b * c)/(6 * a ** 2)) - (d / (2 * a))
second_part = ((c /( 3 * a)) - (b ** 2 / (9 * a ** 2))) ** 3
second_part_in_formula = (first_part ** 2 + second_part) ** (1/2)

solution = (cbrt(first_part + second_part_in_formula) +
            cbrt(first_part - second_part_in_formula) - (b / (3 * a)))

print(f'x = {solution:.2f}')
