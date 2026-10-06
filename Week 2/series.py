'''Series of sums'''
n = int(input())

print('1/2', end='')

for i in range(1, n):
    next_step_num = 2 * (i + 1) - 1
    next_step_den = 2 * (i + 1)
    plus_or_minus = (-1) ** (i + 2)

    if plus_or_minus > 0:
        print(f' + {next_step_num}/{next_step_den}', end='')
    else:
        print(f' - {next_step_num}/{next_step_den}', end='')
print()
