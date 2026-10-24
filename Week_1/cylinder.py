'''Program for calcualting cylinder values'''
from math import pi

radius = float(input("Enter the radius of the cylinder: "))
height = float(input("Enter the height of the cylinder: "))

cylinder_volume = pi * radius ** 2 * height
cylinder_area = 2 * pi * radius * (radius + height)

print(f"V = {cylinder_volume:.3f}")
print(f"A = {cylinder_area:.3f}")
