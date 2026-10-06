'''Tower bloxx the game(khamarochos)'''

score = 15
height = 0
# I FUCKING HATE LINTER
previous_block = ''

while True:
    if score <= 0:
        print(height)
        break

    block = input()

    # Cathing abnormal inputs
    i = 0
    hash_count = 0
    for char in block:
        i += 1
        if char == '#':
            hash_count += 1

    if hash_count > 3 or i > 9:
        break

    if height == 0:
        height += 1
        previous_block = block
        continue

    correct_placement = True

    # To avoid cycling through
    if previous_block == block:
        pass

    else:
        likeness = 0

        now_pos = 0
        for char in block:
            prev_pos = 0
            for prev_char in previous_block:
                if now_pos == prev_pos:
                    if char == prev_char:
                        likeness += 1
                    break
                prev_pos += 1

            now_pos +=1

        # If moved one positon then distrupt two
        if likeness >= 7:
            score -= 1
        elif likeness >= 5:
            score -= 2
        else:
            correct_placement = False
            score -= 3


    if correct_placement:
        height += 1
        previous_block = block
