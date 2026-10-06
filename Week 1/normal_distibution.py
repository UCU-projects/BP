''' Program for evaluating normal distribution '''
from math import e, pi

x = float(input("Enter the value of x: "))
expected_value = float(input("Enter the expected value(𝜇): "))
standard_deviation = float(input("Enter the standard deviation(𝜎): "))

# Using formula to evaluate
normal_distribution =( 1 / (2 * pi * standard_deviation ** 2) ** 0.5
                     * e ** -((x - expected_value) ** 2) / (2 * standard_deviation ** 2))

print(f'{normal_distribution:.10f}')
