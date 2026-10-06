'''Rock paper scissors'''

# With if

for i in range(10):
    game = input()

    if not game:
        break

    first, second = game

    if first == second:
        print('Draw')
    elif game in ('RS', 'PR', 'SP'):
        print(True)
    elif game in ('SR', 'RP', 'PS'):
        print(False)

# With cases

for i in range(10):
    game = input()

    match game:
        case 'RS' | 'PR' |'SP':
            print(True)
        case 'SS'| 'RR' | 'PP':
            print('Draw')
        case '':
            break
        case _:
            print(False)
