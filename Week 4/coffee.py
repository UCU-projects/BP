water = 0
used_water = 0
beans = 0
used_beans = 0

zmih = 0
how_much = 0

ans = input()

if ans == 'on':
    print('[ГОТОВО]')
    print(f'Вода:{water} мл | Зерна:{beans} г')
    while True:
        ans = input('Оберіть команду:')

        if ans == 'off':
            print(f'Приготовано напоїв:{how_much}')
            if how_much > 0:
                print(f'У середньому на напій: {used_water/how_much:.1f} мл води та {used_beans/how_much:.1f} г зерен')
            break

        if ans == 'clean':
            zmih = 0
            print('Контейнер спорожнено.')
            continue

        if zmih >= 4:
            print('Контейнер для жмиху повний. Спорожніть контейнер.')
        elif ans == 'espresso':
            if beans >= 8:
                if water >= 30:
                    how_much += 1
                    beans -= 8
                    water -= 30
                    used_water += 30
                    used_beans += 8
                    zmih += 1
                    print(f'Напій {ans} готовий.')
                else:
                    print('Недостатньо води.')
            else:
                print('Недостатньо зерен.')
        elif ans == 'lungo':
            if beans >= 8:
                if water >= 90:
                    how_much += 1
                    beans -= 8
                    water -= 90
                    used_water += 90
                    used_beans += 8
                    zmih += 1
                    print(f'Напій {ans} готовий.')
                else:
                    print('Недостатньо води.')
            else:
                print('Недостатньо зерен.')
            
        elif ans == 'americano':
            if beans >= 8:
                if water >= 120:
                    how_much += 1
                    beans -= 8
                    water -= 120
                    zmih += 1
                    used_water += 120
                    used_beans += 8

                    print(f'Напій {ans} готовий.')
                else:
                    print('Недостатньо води.')
            else:
                print('Недостатньо зерен.')
        elif ans == 'add water':
            ans = input('Введіть обʼєм води:')
            try:
                ans = int(ans)
            except ValueError:
                print('Введіть додатне ціле число')
                continue

            if ans <= 0:
                print('Введіть додатне ціле число')
            else:
                water += ans 
                print(f'Вода:{water} мл | Зерна:{beans} г')

        elif ans == 'add beans':
            ans = input('Введіть масу зерен:')
            try:
                ans = int(ans)
            except ValueError:
                print('Введіть додатне ціле число')
                continue

            if ans <= 0:
                print('Введіть додатне ціле число')
            else:
                beans += ans 
                print(f'Вода: {water} мл | Зерна:{beans} г')
            
        else: 
            print('НЕВІДОМА КОМАНДА')
        
print('[МАШИНА ВИМКНЕНА]')