'''Program for creating triangle with numbers'''
first_num = int(input())
height = int(input())

for i in range(1, height+1):
    print(*range(first_num, first_num + height + 1 - i))
