ans = input()

if ans == 'start':
    print("ІНІЦІАЛІЗАЦІЯ БАНКОМАТУ")
    print('Працівник банку поповнює банкомат купюрами:')

    m1000 = int(input('Кількість банкнот номіналом 1000 грн: '))
    m500 = int(input('Кількість банкнот номіналом 500 грн: '))
    m200 = int(input('Кількість банкнот номіналом 200 грн: '))
    m100 = int(input('Кількість банкнот номіналом 100 грн: '))
    m50 = int(input('Кількість банкнот номіналом 50 грн: '))
    m10 = int(input('Кількість банкнот номіналом 10 грн: '))

    total = m1000 * 1000 + m500 * 500 + m200 * 200 + m100 * 100 + m50 * 50 + m10 * 10

    print(f'Банкомат ініціалізовано. Загальна сума: {total} грн')
    print('=== БАНКОМАТ ПРАЦЮЄ ===')

    while total > 0: 
        money = input('Вставте картку (зчитується баланс картки): ')

        if money == 'quit':
            print('Банкомат відключено працівником.')
            break

        try:
            money = int(money)
        except ValueError:
            print('Некоректна сума. Введіть додатне ціле число.')
            continue

        if money > 0:
            print(f'Доступний залишок на картці {money} грн.')

            while True:
                if total <= 0:
                    break

                ans = input('Введіть суму для зняття або q: ')

                if total < 0: 
                    break

                if ans == 'q':
                    print('Операцію скасовано. Наступний клієнт.')
                    break
        
                try:
                    ans = int(ans)
                except ValueError:
                    print('Некоректна сума. Введіть додатне ціле число.') 
                    continue

                if ans > money: 
                    print(f'Доступний залишок на картці {money} грн. Введіть відповідну суму.')
                elif ans > total:
                    print(f'Доступний залишок в банкоматі {total} грн. Введіть відповідну суму.')
                elif ans <= 0:
                    print('Некоректна сума. Введіть додатне ціле число.')
                else:
                    if money - ans < 0:
                        break

                    if total - ans < 0:
                        break

                    else:
                        money -= ans
                        total -= ans
                        if money == 0:
                            print(f'Видано {ans} грн. На картці немає коштів.')
                            break
                        else:
                            print(f'Видано {ans} грн. Залишок на картці: {money} грн.')
                    
        elif money == 0:
            print('На рахунку немає коштів.')
        else:
            print('Некоректна сума. Введіть додатне ціле число.')

print('=== БАНКОМАТ НЕ ПРАЦЮЄ ===')