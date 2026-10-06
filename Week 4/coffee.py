''' Coffee machine simulator '''

from time import sleep
from random import randint

# Resources
WATER_CAPACITY = 1500
water = 0
used_water = 0

BEANS_CAPACITY = 300
beans = 0
used_beans = 0

# Clear
zmih = 0
zmih_cleared = 0

#Stats
espresso_counter = 0
americano_counter = 0
lungo_counter = 0
denied_counter = 0
error_counter = 0

#Other
debug = False
calcium = 0
beans_in_mill = 0
# Wrapping this string in raw so python don't label as syntax error because of '/'
COFFEE_ASCII = r"""
                     (
                       )   (
          ___...(-------)-....___
      .-""        )    (         ""-.
.-'``'|-._               )         _.-|
 /  .--.|    `""---...........---""`  |
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

# Pluses because of so many "'"

ans = input()

if ans == 'on':
    print('[ГОТОВО]')
    print(f'Вода: {water} мл | Зерна: {beans} г')
    while True:
        # Truly random error
        chance = randint(1, 1000)
        if chance == 333:
            print('[ERROR: TERMINATED]')
            break

        # If five times unknown command in a row then break
        if error_counter == 5:
            print('Ой, кавомашина вийшла з ладу. Cхоже вона перегрілась')
            break

        # Debug purely cosmetic, just for stats and in-manchine understanding errors
        if debug:
            print(f'Приготовано еспресо:{espresso_counter} |'
                  f'американо: {americano_counter} | лунго: {lungo_counter}')
            print(f'У загальному кількість використаних води: {used_water} мл'
                  f'та зерен: {used_beans} г')

        ans = input('Оберіть команду: ')

        taste_msg = f'Над {ans} підіймається запашний димок, кава вийшла на славу.'
        coffee_power = 1

        # Establishing values to another cycle
        if calcium >= 10:
            taste_msg = f'Йойки, {ans} вийшов поганеньким на смак.'
            if debug:
                print('НЕОБХІДНА ДЕКАЛЬНІЗАЦІЯ')

        # Exiting and loading stats
        if ans == 'off':
            error_counter = 0
            drink_counter = espresso_counter + americano_counter + lungo_counter
            favourite_drink = max(espresso_counter, americano_counter, lungo_counter)
            print(f'Приготовано напоїв: {drink_counter}')
            if drink_counter > 0:
                print(f'Приготовано еспресо:{espresso_counter}'
                      f'| американо: {americano_counter} | лунго: {lungo_counter}')
                #Python must check in and two values but remembers only last one
                #using this to print favourite drink
                _ = (favourite_drink == espresso_counter and 'espresso' or
                     favourite_drink == americano_counter and 'americano' or
                     favourite_drink == lungo_counter and 'lungo')

                print(f'Найпопулярніший напій: {_}')
                print(f'У середньому на напій: {used_water/drink_counter:.1f} мл води'
                      f'та {used_beans/drink_counter:.1f} г зерен')
                print(f'У загальному кількість використаних води: {used_water} мл'
                      f'та зерен: {used_beans} г')
                print(f'Кількість чищень контейнера для жмиху: {zmih_cleared}')
                print(f'Кількість відмов у приготуванні через нестачу ресурсів: {denied_counter}')
            break

        if ans == 'clean':
            error_counter = 0
            zmih = 0
            zmih_cleared += 1
            print('Контейнер спорожнено.')
            continue

        # Brewing coffee
        if zmih >= 4:
            print('Контейнер для жмиху повний. Спорожніть контейнер.')
        elif beans_in_mill >= 20 and ans in ('espresso' , 'lungo', 'americano'):
            print(f'Упс, на жаль, не можу приготувати {ans}, схоже млинок не працює.')
            if debug:
                print('НЕ МОЖУ ОБЕРНУТИ МЛИНОК.')
        elif ans == 'espresso':
            error_counter = 0
            # Button to power up coffee
            while True:
                if coffee_power > 3:
                    print('Припиніть, вас зараз серцевий напад хапить!')
                    break

                choice = input('Хочете зробити каву міцнішою(+8г)(y/n): ')
                if choice == 'y':
                    coffee_power += 1
                else:
                    break

            if beans >= 8*coffee_power:
                if water >= 30:
                    calcium += 1
                    beans_in_mill += 1 * coffee_power
                    espresso_counter += 1
                    beans -= 8 * coffee_power
                    water -= 30
                    used_water += 30
                    used_beans += 8 * coffee_power
                    zmih += 1

                    print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                else:
                    denied_counter += 1
                    print('Недостатньо води.')
            else:
                denied_counter += 1
                # Smart alternative for powered-up coffee
                if beans >= 8 and water >= 30:
                    choice = input(f'Не вистачає зерен. Можу зробити звичайний {ans}'
                                   f'без +{coffee_power*8}г зерен(y/n): ')
                    if choice == 'y':
                        coffee_power = 1
                        calcium += 1
                        beans_in_mill += 1 * coffee_power
                        espresso_counter += 1
                        beans -= 8 * coffee_power
                        water -= 30
                        used_water += 30
                        used_beans += 8 * coffee_power
                        zmih += 1

                        print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                        continue

                print('Не вистачає зерен')
        elif ans == 'lungo':
            error_counter = 0
            while True:
                if coffee_power > 3:
                    print('Припиніть, вас зараз серцевий напад хапить!')
                    break

                choice = input('Хочете зробити каву міцнішою(+8г)(y/n): ')
                if choice == 'y':
                    coffee_power += 1
                else:
                    break

            if beans >= 8*coffee_power:
                if water >= 90:
                    calcium += 1
                    beans_in_mill += 1 * coffee_power
                    lungo_counter += 1
                    beans -= 8 * coffee_power
                    water -= 90
                    used_water += 90
                    used_beans += 8 * coffee_power
                    zmih += 1

                    print(f'Напій {ans} готовий.'
                          f'{taste_msg}\n {COFFEE_ASCII}')
                else:
                    denied_counter += 1
                    # Smart alternative for just coffee
                    if water >= 30:
                        choice = input(f'Недостатньо води для {ans}.'
                                       f'Пропоную приготувати espresso натомість. (y/n): ')
                        if choice == 'y':
                            coffee_power = 1
                            ans = 'espresso'
                            espresso_counter += 1
                            beans -= 8 * coffee_power
                            water -= 30
                            used_water += 30
                            used_beans += 8 * coffee_power
                            zmih += 1
                            calcium += 1
                            beans_in_mill += 1 * coffee_power

                            print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                            continue

                    print('Не вистачає води')

            else:
                denied_counter += 1
                if beans >= 8 and water >= 90:
                    choice = input(f'Не вистачає зерен. Можу зробити звичайний {ans}'
                                   f'без +{coffee_power*8}г зерен(y/n): ')
                    if choice == 'y':
                        coffee_power = 1
                        calcium += 1
                        beans_in_mill += 1 * coffee_power
                        espresso_counter += 1
                        beans -= 8 * coffee_power
                        water -= 90
                        used_water += 90
                        used_beans += 8 * coffee_power
                        zmih += 1
                        print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                        continue

                print('Не вистачає зерен')
        elif ans == 'americano':
            error_counter = 0
            while True:
                if coffee_power > 3:
                    print('Припиніть, вас зараз серцевий напад хапить!')
                    break

                choice = input('Хочете зробити каву міцнішою(+8г)(y/n): ')
                if choice == 'y':
                    coffee_power += 1
                else:
                    break

            if beans >= 8*coffee_power:
                if water >= 120:
                    americano_counter += 1
                    beans -= 8 * coffee_power
                    water -= 120
                    used_water += 120
                    used_beans += 8 * coffee_power
                    zmih += 1
                    calcium += 1
                    beans_in_mill += 1 * coffee_power

                    print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                else:
                    denied_counter += 1
                    if water >= 90:
                        choice = input(f'Недостатньо води для {ans}.'
                                       'Пропоную приготувати lungo натомість. (y/n): ')
                        if choice == 'y':
                            coffee_power = 1
                            ans = 'lungo'
                            lungo_counter += 1
                            beans -= 8 * coffee_power
                            water -= 90
                            used_water += 90
                            used_beans += 8 * coffee_power
                            zmih += 1
                            calcium += 1
                            beans_in_mill += 1 * coffee_power

                            print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                            continue

                    print('Не вистачає води')
            else:
                denied_counter += 1
                if beans >= 8 and water >= 120:
                    choice = input(f'Не вистачає зерен. Можу зробити звичайний {ans}'
                                   f'без +{coffee_power*8 - 8}г зерен(y/n): ')
                    if choice == 'y':
                        coffee_power = 1
                        calcium += 1
                        beans_in_mill += 1 * coffee_power
                        espresso_counter += 1
                        beans -= 8 * coffee_power
                        water -= 120
                        used_water += 120
                        used_beans += 8 * coffee_power
                        zmih += 1

                        print(f'Напій {ans} готовий. {taste_msg}\n {COFFEE_ASCII}')
                        continue

                print('Не вистачає зерен')
        # Adding resources commands
        elif ans == 'add water':
            error_counter = 0
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
                print(f'Контейнер для води переповнений. Додано {WATER_CAPACITY - water} мл води.'
                      f'Вилилось {ans + water - WATER_CAPACITY} мл води.')
                water = WATER_CAPACITY
            else:
                water += ans

            print(f'Вода:{water} мл | Зерна: {beans} г')

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
                print(f'Контейнер для зерен переповнений. Додано {BEANS_CAPACITY - beans} г зерен.'
                      f'Висипалось {ans + beans - BEANS_CAPACITY} г зерен.')
                beans = BEANS_CAPACITY
            else:
                beans += ans

            print(f'Вода: {water} мл | Зерна: {beans} г')

        elif ans == 'fill':
            error_counter = 0
            water_msg, beans_msg = '', ''

            water += WATER_CAPACITY
            beans += BEANS_CAPACITY

            if water >= WATER_CAPACITY:
                water_msg = ('Контейнер для води переповнений. '
                             f'Додано {2 * WATER_CAPACITY - water} мл води.'
                             f'Вилилось {water - WATER_CAPACITY} мл води.')
                water = WATER_CAPACITY

            if beans >= BEANS_CAPACITY:
                beans_msg = ('Контейнер для зерен переповнений. '
                             f'Додано {2 * BEANS_CAPACITY - beans} г зерен.'
                             f'Висипалось {beans - BEANS_CAPACITY} г зерен.')
                beans = BEANS_CAPACITY

            print(f'{water_msg} {beans_msg}')

            print(f'Вода: {water} мл | Зерна: {beans} г')

        # Service mode
        elif ans == 'master':
            error_counter = 0
            print(f'Вода: {water} мл | Зерна: {beans} г')
            print(f'Приготовано напоїв: {espresso_counter + americano_counter + lungo_counter}')
            print(f'Приготовано еспресо: {espresso_counter} | '
                  f'американо: {americano_counter} | лунго: {lungo_counter}')
            print(f'Кількість чищень контейнера для жмиху: {zmih_cleared}')
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

            choice = input('Ви впевнені, що хочете скинути лічильники? (y/n): ')
            if choice == 'y':
                espresso_counter = 0
                americano_counter = 0
                lungo_counter = 0
                zmih_cleared = 0
                denied_counter = 0
                used_water = 0
                used_beans = 0
                error_counter = 0

            # Using built-in time library to step by step print '.'
            choice = input('Ви хочете провести технічне обслуговування? (y/n): ')
            if choice == 'y':
                print('Спустошую контейнери для води та зерен.', end='')
                for i in range(2):
                    # Using flush in order to avoid memory leakage
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Мию контейнери для води та зерен.', end='')
                for i in range(3):
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Спустошую контейнер для жмиху.', end='')
                zmih = 0
                for i in range(1):
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Дістаю фільтр, чищу його від кальцію та мию.', end='')
                calcium = 0
                for i in range(4):
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Дістаю млинок, розбираю його та чищу.', end='')
                beans_in_mill = 0
                for i in range(5):
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Збираю всі деталі та встановлюю їх на місце.', end='')
                for i in range(10):
                    print('.', end='', flush=True)
                    sleep(1)
                print()

                print('Технічне обслуговування завершено.')

        else:
            error_counter += 1
            print('[НЕВІДОМА КОМАНДА]')

print('[МАШИНА ВИМКНЕНА]')
