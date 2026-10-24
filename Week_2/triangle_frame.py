''' Program for creating triangle frame'''
height = int(input())

for i in range(1, height+1):
    if i == height:
        print("*" * i)
    elif i > 2:
        print('*' + ' ' * (i - 2) + '*')
    else:
        print('*' * i)
