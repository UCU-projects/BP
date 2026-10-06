'''One of lab works, diffrent from prevoius by aligning to right'''
# Filtering basic input errors
while True :
    n = input()
    try:
        n = int(n)
    except ValueError:
        continue

    # not in one block, less try - better
    if 1 <= n <= 26:
        break
    else:
        continue

# Counting how many iterations needed
_ = 0
total_row_count = 0
while _ < n:
    total_row_count += 1
    _ += total_row_count


# Starting with 65 which is "A"
letter_value = 0

for row in range(1, total_row_count+1): # Starting with one to avoid empty line at the start
    if letter_value >= n:
        break

    space = (total_row_count - row) * 2 # Two here because each space letter, so twice needed
    print(' ' * space, end='')

    for col in range(row):
        if letter_value >= n:
            break

        if col == 0:
            print(chr(65 + letter_value), end='')
        else:
            print(' ' + chr(65 + letter_value), end='')

        # To cycle through alphabet
        letter_value += 1

    print()
