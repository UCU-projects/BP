'''Loading simulator'''
load_box = 0
reweight_box = 0
wait_box = 0

box_weight = 0
lorry_weight = float(input())

while True:
    box = input()

    if box == 'q':
        break

    try:
        box = float(box)
    except ValueError:
        reweight_box += 1
        continue

    if box <= 0:
        reweight_box += 1
    elif box_weight + box <= lorry_weight:
        box_weight += box
        load_box += 1
    else:
        wait_box += 1

print(load_box)
print(reweight_box)
print(wait_box)
