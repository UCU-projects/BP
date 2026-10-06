'''Program for calculating cosh'''
from math import cosh, e, exp

x = float(input("Enter x: "))

print(f"cosh_lib = {cosh(x):.4f}")
print(f"cosh_exp = {(exp(x) + exp(-x))/2:.4f}")
print(f"cosh_e = {(e ** x + e ** -x)/2:.4f}")
