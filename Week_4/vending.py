'''Vending machine simulator'''

COST_DRINK = 25
total = 0
total_quantity, quantity = 0, 0
i = 0
ans = input()

if ans == 'start':
    i = 1
    print('ІНІЦІАЛІЗАЦІЯ ТОРГОВОГО АВТОМАТУ')
    print('Працівник заповнює автомат напоями та готівкою для решти:')
    quantity = int(input(f'Кількість напоїв (ціна {COST_DRINK} грн за штуку): '))
    total_quantity = quantity

    quantity_5 = int(input('Готівка номіналом 5 грн (кількість купюр): '))
    quantity_10 = int(input('Готівка номіналом 10 грн (кількість купюр): '))
    quantity_20 = int(input('Готівка номіналом 20 грн (кількість купюр): '))
    quantity_50 = int(input('Готівка номіналом 50 грн (кількість купюр): '))
    quantity_100 = int(input('Готівка номіналом 100 грн (кількість купюр): '))


    total = (
        quantity_100 * 100
        + quantity_50 * 50
        + quantity_20 * 20
        + quantity_10 * 10
        + quantity_5 * 5
    )

    print('Автомат ініціалізовано.')
    print(f'Кількість напоїв: {quantity}. Готівка: {total} грн')
    print('=== ТОРГОВИЙ АВТОМАТ ПРАЦЮЄ ===')

    while quantity != 0:
        ans = input('Внесіть кошти (сума): ')

        if ans == 'quit':
            print('Автомат відключено працівником.')
            break

        try:
            money = int(ans)
        except ValueError:
            break

        print(f'Внесено коштів: {money} грн.')
        print(f'Напій коштує {COST_DRINK} грн. Залишилось напоїв: {quantity}')

        while True:
            ans = input('Укажіть кількість напоїв до покупки'
                        ' або q для припинення роботи (кошти повертаються): ')

            if ans == 'q':
                print(f'Решта: {money} грн. Наступний клієнт.')
                break

            try:
                ans = int(ans)
            except ValueError:
                print('Некоректна кількість. Введіть додатнє ціле число.')
                continue

            if ans <= 0:
                print('Некоректна кількість. Введіть додатнє ціле число.')
                continue

            if ans > quantity:
                print(f'Доступно лише {quantity} напоїв. Введіть відповідну кількість.')
                continue

            how_much = ans * COST_DRINK

            if how_much > money:
                print(f'Недостатньо коштів. Потрібно {how_much} грн, а у вас {money} грн.')
                continue

            total += how_much
            money -= how_much
            quantity -= ans

            print(f'Видано напоїв: {ans} штук. Доступні кошти: {money} грн.')

            if quantity == 0:
                print(f'Решта: {money} грн.')
                break

            if money == 0:
                print(f'Решта: {money} грн. Наступний клієнт.')
                break

if i == 1:
    print(f'Кількість виданих напоїв: {total_quantity - quantity}. Готівка: {total} грн')
print('=== ТОРГОВИЙ АВТОМАТ НЕ ПРАЦЮЄ ===')
