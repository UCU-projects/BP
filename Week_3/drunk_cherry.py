'''CAS for drunk cherry '''
total_volume = 0
glass_cherry_volume = 0
glass_volume = 0
given_glass = False

# Variables for glass filling
cherry_volume = 0
alcohole_volume = 0


# If customer nefarious joker
while True:
    height = input()
    weight = input()
    try:
        weight = float(weight)
        height = float(height)
    except ValueError:
        continue
    else:
        if weight > 0 and height > 0:
            break
        else:
            continue

max_volume = 5 * height * weight

# Pouring station
while True:
    ans = input()

    if ans == 'q':
        if glass_volume > 0 and glass_cherry_volume / glass_volume > 0.15:
            print('Перевищено ліміт вишень')
            break
        print(total_volume)
        break

    # Creating new glass
    if ans == 'U':
        given_glass = True

        # Check if previous glass have less than 15 percent of cherries
        if glass_volume > 0 and glass_cherry_volume / glass_volume > 0.15:
            print('Перевищено ліміт вишень')
            break

        glass_cherry_volume = 0
        glass_volume = 0
        continue

    # Variables for parsing pouring input
    is_hash = False
    is_cherry = False
    is_x = False
    num_str = ""

    # Cycling through input to choose what to do and how
    for char in ans:
        # Accounting for not having glass
        if not given_glass:
            break

        if char == '#':
            is_hash = True
        # Filtering zeroes if "#x0"
        elif char == '0' and not is_x and not is_hash:
            is_cherry = True
        elif char == 'x':
            is_x = True
        elif char >= '0' and char <= '9':
            num_str = num_str + char

    if num_str == '':
        NUMBER = 1
    else:
        NUMBER = int(num_str)


    if is_hash:
        alcohole_volume += 20 * NUMBER
    elif is_cherry:
        cherry_volume += 5 * NUMBER

    glass_cherry_volume += cherry_volume
    glass_volume += (cherry_volume + alcohole_volume)
    total_volume += (cherry_volume + alcohole_volume)

    if glass_volume > 500:
        print('Збій роботи датчика')
        break
    elif total_volume > max_volume:
        print('Перевищено ліміт алкоголю')
        break

    cherry_volume = 0
    alcohole_volume = 0
