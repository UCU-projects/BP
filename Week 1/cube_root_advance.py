'''Program for calculating all solutions of cubic'''
from math import cbrt

a = float(input("Enter first coefficient: "))
b = float(input("Enter second coefficient: "))
c = float(input("Enter third coefficient: "))
d = float(input("Enter fourth coefficient: "))

# Optimizing formula because of repeated parts(Cardano)
first_part = -b ** 3 / (27 * a ** 3) + (b * c) / (6 * a ** 2) - d / (2 * a)
second_part = (c / (3 * a) - b ** 2 / (9 * a ** 2)) ** 3
second_part_in_formula = first_part ** 2 + second_part

if second_part_in_formula >= 0:
    second_part_in_formula = second_part_in_formula ** (1/2)
    u = cbrt(first_part + second_part_in_formula)
    v = cbrt(first_part - second_part_in_formula)
    solution1 = u + v - b / (3 * a)
else:
    u = cbrt((first_part + second_part_in_formula))
    v = cbrt((first_part - second_part_in_formula))
    solution1 = (u + v) - b / (3 * a)

# Horner scheme
coefficient1 = a
coefficient2 = b + coefficient1 * solution1
coefficient3 = c + coefficient2 * solution1

# Using discriminant formula
discriminant = coefficient2 ** 2 - 4 * coefficient1 * coefficient3
solution2 = (-coefficient2 + discriminant ** (1/2)) / 2 * coefficient1
solution3 = (-coefficient2 - discriminant ** (1/2)) / 2 * coefficient1

print(f'x1 = {solution1:.2f}')
print(f'x2 = {solution2:.2f}')
print(f'x3 = {solution3:.2f}')
