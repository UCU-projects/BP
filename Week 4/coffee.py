WATER_CAPACITY = 1500
water = 0
used_water = 0

BEANS_CAPACITY = 300
beans = 0
used_beans = 0

zmih = 0
zmih_cleared = 0

espresso_counter = 0
americano_counter = 0
lungo_counter = 0
denied_counter = 0

debug = False
calcium = 0
beans_in_mill = 0
coffee_ascii = """
                     (
                       )   (
          ___...(-------)-....___
      .-""        )    (         ""-.
.-'``'|-._               )         _.-|
 /  .--.|    `""---...........---""`   |
/  /    |                            |
|  |    |                            |
 \  \   |                            |
  `\ `\ |                            |
    `\ `|                            |
     _/ /\                           /
    (__/  \                         /
 _..---""` \                       /`""---.._
.-'         \                   /          '-.
:             `-.__         __.-'             :
:               ) ""---...---"" (             :
 '._            `"--...___...--"`          _.'
    \\"--..__                    __..--""/
   '._""" + '"""----.....______.....----""" _.' + """
        `""--..,,_____         _____,,..--""`
                     `""" + '"""----"""`'

ans = input()

if ans == 'on':
    print('[ГОТОВО]')
    print(f'Вода: {water} мл | Зерна: {beans} г')
    while True:
        if debug:
            print(f'Приготовано еспресо:{espresso_counter} | американо: {americano_counter} | лунго: {lungo_counter}')
            print(f'У загальному кількість використаних води: {used_water} мл та зерен: {used_beans} г')
        ans = input('Оберіть команду: ')
        
        if calcium >= 10:
            taste_msg = f'Йойки, {ans} вийшов поганеньким на смак'
            if debug:
                print('НЕОБХІДНА ДЕКАЛЬНІЗАЦІЯ')
        taste_msg = f'Над {ans} підіймається запашний димок, кава вийшла на славу.'

        if ans == 'off':
            drink_counter = espresso_counter + americano_counter + lungo_counter
            favourite_drink = max(espresso_counter, americano_counter, lungo_counter)
            print(f'Приготовано напоїв: {drink_counter}')
            if drink_counter > 0:
                print(f'Приготовано еспресо:{espresso_counter} | американо: {americano_counter} | лунго: {lungo_counter}')
                print(f'Найпопулярніший напій: {favourite_drink == espresso_counter and 'espresso' or favourite_drink == americano_counter and 'americano' or favourite_drink == lungo_counter and 'lungo'}')
                print(f'У середньому на напій: {used_water/drink_counter:.1f} мл води та {used_beans/drink_counter:.1f} г зерен')
                print(f'У загальному кількість використаних води: {used_water} мл та зерен: {used_beans} г')
                print(f'Кількість чищеннь контейнера для жмиху: {zmih_cleared}')
                print(f'Кількість відмов у приготуванні через нестачу ресурсів: {denied_counter}')
            break

        if ans == 'clean':
            zmih = 0
            zmih_cleared += 1
            print('Контейнер спорожнено.')
            continue

        # Brewing coffee
        if zmih >= 4:
            print('Контейнер для жмиху повний. Спорожніть контейнер.')
        elif beans_in_mill > 5 and ans in ('espresso' , 'lungo', 'americano'):
            print(f'Упс, на жаль, не можу приготувати {ans}, схоже млинок не працює.')
            if debug:
                print('ЗЕРНА ЗАСТРЯГЛИ')
        elif ans == 'espresso':
            if beans >= 8:
                if water >= 30:
                    calcium += 1
                    beans_in_mill += 1
                    espresso_counter += 1
                    beans -= 8
                    water -= 30
                    used_water += 30
                    used_beans += 8
                    zmih += 1

                    print(f'Напій {ans} готовий. {taste_msg}\n {coffee_ascii}')
                else:
                    denied_counter += 1
                    print('Недостатньо води.')
            else:
                denied_counter += 1
                print('Недостатньо зерен.')
        elif ans == 'lungo':
            if beans >= 8:
                if water >= 90:
                    calcium += 1
                    beans_in_mill += 1
                    lungo_counter += 1
                    beans -= 8
                    water -= 90
                    used_water += 90
                    used_beans += 8
                    zmih += 1

                    print(f'Напій {ans} готовий. {taste_msg}\n {coffee_ascii}')
                else:
                    denied_counter += 1
                    if water >= 30:
                        choice = input(f'Недостатньо води для {ans}. Пропоную приготувати espresso натомість. (y/n): ')
                        if choice == 'y':
                            ans = 'espresso'
                            espresso_counter += 1
                            beans -= 8
                            water -= 30
                            used_water += 30
                            used_beans += 8
                            zmih += 1
                            calcium += 1
                            beans_in_mill += 1

                            print(f'Напій {ans} готовий. {taste_msg}\n {coffee_ascii}')
                            continue

                    print('Недостатньо води.')
            else:
                denied_counter += 1
                print('Недостатньо зерен.')
            
        elif ans == 'americano':
            if beans >= 8:
                if water >= 120:
                    americano_counter += 1
                    beans -= 8
                    water -= 120
                    used_water += 120
                    used_beans += 8
                    zmih += 1
                    calcium += 1
                    beans_in_mill += 1

                    print(f'Напій {ans} готовий. {taste_msg}\n {coffee_ascii}')
                else:
                    denied_counter += 1
                    if water >= 90:
                        choice = input(f'Недостатньо води для {ans}. Пропоную приготувати lungo натомість. (y/n): ')
                        if choice == 'y':
                            ans = 'lungo'
                            lungo_counter += 1
                            beans -= 8
                            water -= 90
                            used_water += 90
                            used_beans += 8
                            zmih += 1
                            calcium += 1
                            beans_in_mill += 1

                            print(f'Напій {ans} готовий. {taste_msg}\n {coffee_ascii}')
                            
                            continue

                    print('Недостатньо води.')
            else:
                denied_counter += 1
                print('Недостатньо зерен.')

        # Adding resources commands 
        elif ans == 'add water':
            ans = input('Введіть обʼєм води: ')

            try:
                ans = int(ans)
            except ValueError:
                print('Введіть додатне ціле число')
                continue

            if ans <= 0:
                print('Введіть додатне ціле число')
                continue

            if ans + water >= WATER_CAPACITY:
                print(f'Контейнер для води переповнений. Додано {WATER_CAPACITY - water} мл води. Вилилось {ans + water - WATER_CAPACITY} мл води.')
                water = WATER_CAPACITY
            else:
                water += ans 

            print(f'Вода:{water} мл | Зерна:  {beans} г')

        elif ans == 'add beans':
            ans = input('Введіть масу зерен: ')

            try:
                ans = int(ans)
            except ValueError:
                print('Введіть додатне ціле число')
                continue

            if ans <= 0:
                print('Введіть додатне ціле число')
                continue

            if ans + beans >= BEANS_CAPACITY:
                print(f'Контейнер для зерен переповнений. Додано {BEANS_CAPACITY - beans} г зерен. Висипалось {ans + beans - BEANS_CAPACITY} г зерен.')
                beans = BEANS_CAPACITY
            else:
                beans += ans 
                
            print(f'Вода: {water} мл | Зерна: {beans} г')

        elif ans == 'fill':
            water += WATER_CAPACITY
            beans += BEANS_CAPACITY

            if water >= WATER_CAPACITY:
                water_msg = f'Контейнер для води переповнений. Додано {2 * WATER_CAPACITY - water} мл води. Вилилось {water - WATER_CAPACITY} мл води.'   
                water = WATER_CAPACITY

            if beans >= BEANS_CAPACITY:
                beans_msg = f'Контейнер для зерен переповнений. Додано {2 * BEANS_CAPACITY - beans} г зерен. Висипалось {beans - BEANS_CAPACITY} г зерен.'
                beans = BEANS_CAPACITY

            if water_msg or beans_msg:
                print(f'{water_msg} {beans_msg}')

            print(f'Вода: {water} мл | Зерна: {beans} г')

        elif ans == 'master':
            print(f'Вода: {water} мл | Зерна: {beans} г')
            print(f'Приготовано напоїв: {espresso_counter + americano_counter + lungo_counter}')
            print(f'Приготовано еспресо: {espresso_counter} | американо: {americano_counter} | лунго: {lungo_counter}')
            print(f'Кількість чищеннь контейнера для жмиху: {zmih_cleared}')
            print(f'Кількість відмов у приготуванні через нестачу ресурсів: {denied_counter}')
            if debug:
                print('Режим налагодження увімкнено.')
                choice = input('Ви хочете вимкнути режим налагодження? (y/n): ')
                if choice == 'y':
                    debug = False
            else:     
                choice = input('Ви впевнені, що хочете увімкнути режим налагодження? (y/n): ')
                if choice == 'y':
                    debug = True

            choice = input('Ви впевнені, що хочете скинути лічильки? (y/n): ')
            if choice == 'y':
                espresso_counter = 0
                americano_counter = 0
                lungo_counter = 0
                zmih_cleared = 0
                denied_counter = 0
                used_water = 0
                used_beans = 0

            choice = input('Ви хочете провести технічне обслуговування? (y/n): ')
            if choice == 'y':
                print('Спустошую контейнери для води та зерен.', end='')
                for i in range(2):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Мию контейнери для води та зерен.', end='')
                for i in range(3):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Спустошую контейнер для жмиху.', end='')
                zmih = 0
                zmih_cleared += 1
                for i in range(1):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Дістаю фільтр, чищу його від кальцію та мию.', end='')
                calcium = 0
                for i in range(4):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Дістаю млинок, розбираю його та чищу.', end='')
                beans_in_mill = 0
                for i in range(5):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Збираю всі деталі та встановлюю їх на місце.', end='')
                for i in range(10):
                    print('.', end='', flush=True)
                    for _ in range(20_000_000):
                        pass
                print()

                print('Технічне обслуговування завершено.')

        else: 
            print('[НЕВІДОМА КОМАНДА]')    


print('[МАШИНА ВИМКНЕНА]')