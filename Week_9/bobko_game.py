"""
RPG
"""

import sys
import random
import os
from functools import partial

BOLD = '\033[1m'
RED = '\033[31m'
GREEN= '\033[32m'
NC= '\033[0m'

# === INITITALIZATION LOGIC ===

def create_player() -> dict:
    '''
    Creating player state

    :return : dict, A dictionary with all crucial player variables
    '''

    return {
        'name': "", 'race': "", 'c_class': "", 'crit_damage': 1,
        'lvl': 1, 'exp': 0, 'cap_exp': 100, 'hp': 0, 'mp': 0,
        'hp_max': 0, 'mp_max': 0, 'defense': 1, 'strength': 0, 'mag_strength': 0,
        'gold': 0, 'inventory': set(), 'location': [1, 1], 'entry_direction': '',
        'spell_book': {}, 'estus': 1, 'ashen': 1, 'boss_item': False,
        'last_message': '', 'class_m': 0
    }


def create_enemy(name:str, hp:int, mp:int, defense:int, strength:int,
                mag_strength:int, spell_book:list, location:tuple) -> dict:
    """
    Creating enemy state

    :param name: str, name of the enemy
    :param hp: int, health points of the enemy
    :param mp: int, mana points of the enemy
    :param defense: int, defense points of the enemy
    :param strength: int, strength points of the enemy
    :param mag_strength: int, magic strength points of the enemy
    :param spell_book: list, list of spells the enemy can cast
    :param location: tuple, (x, y) coordinates of the enemy on the map

    :return: dict, A dictionary with all crucial enemy variables
    """
    return {
        'type': 'enemy', 'name': name, 'hp': hp, 'mp': mp, 'hp_max': hp, 'mp_max': mp,
        'defense': defense, 'str': strength, 'mag_str': mag_strength, 'spell_book': spell_book,
        'location': list(location), 
        'gold': random.randint(round(10+strength+defense+mag_strength),
                                round(50+strength+mag_strength+defense)),
        'exp': random.randint(round(strength+10+defense+mag_strength),
                               round(100+defense+mag_strength+strength)),
        'last_message': ''
    }


def create_boss(name, hp, mp, defense, strength, mag_str, spell_book):
    """
    Creating boss state

    :param name: str, name of the boss
    :param hp: int, health points of the boss
    :param mp: int, mana points of the boss
    :param defense: int, defense points of the boss
    :param strength: int, strength points of the boss
    :param mag_str: int, magic strength points of the boss
    :param spell_book: list, list of spells the boss can cast

    :return: dict, A dictionary with all crucial boss variables
    """
    return {
        'type': 'boss', 'name': name, 'hp': hp, 'mp': mp, 'hp_max': hp, 'mp_max': mp,
        'defense': defense, 'str': strength, 'mag_str': mag_str, 'spell_book': spell_book,
        'gold': random.randint(100, 200), 'exp': random.randint(100, 150), 'last_message': ''
    }


def create_town(location:tuple) -> dict:
    """
    Creating town state

    :param name: str, name of the town
    :param location: tuple, (x, y) coordinates of the town on the map

    :return: dict, A dictionary with all crucial town variables
    """

    return {
        'location': list(location)
    }


def create_dungeon(location:tuple, boss:dict) -> dict:
    """
    Creating dungeon state

    :param location: tuple, (x, y) coordinates of the dungeon on the map
    :param boss: dict, the boss that resides in the dungeon

    :return: dict, A dictionary with all crucial dungeon variables
    """
    return {
        'location': list(location), 'boss': boss
    }


def create_game_map(height: int, width: int) -> dict:
    """
    Creating game map state

    :param height: int, height of the map
    :param width: int, width of the map 

    :return : dict, A dictionary with all crucial map variables
    """


    m = [['.' for x in range(width)] for y in range(height)]


    g_map = {'height': height, 'width': width, 'map': m,
            'town_location': None, 'dungeon_location': None
            }

    town_location = list(get_random_empty_location(g_map))
    dungeon_location = list(get_random_empty_location(g_map))

    g_map['town_location'] = town_location
    g_map['dungeon_location'] = dungeon_location

    if g_map['town_location'] == g_map['dungeon_location']:
        g_map['dungeon_location'] = list(get_random_empty_location(g_map))

    return g_map


# === PLAYER LOGIC ===


def apply_elf(player: dict) -> None:
    """
    Applies elf racial traits to the player

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state with elf racial traits
    """

    player['race'] = 'Elf'
    player['hp'] = 70
    player['mp'] = 150
    player['str'] = 3
    player['mag_str'] = 10
    player['defense'] = 0.6


def apply_human(player: dict) -> None:
    """
    Applies human racial traits to the player

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state with human racial traits
    """

    player['race'] = 'Human'
    player['hp'] = 100
    player['mp'] = 100
    player['str'] = 10
    player['mag_str'] = 5
    player['defense'] = 1


def apply_dwarf(player: dict) -> None:
    """
    Applies dwarf racial traits to the player

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state with dwarf racial traits
    """

    player['race'] = 'Dwarf'
    player['hp'] = 150
    player['mp'] = 30
    player['str'] = 12
    player['mag_str'] = 3
    player['defense'] = 1.5


def apply_warrior(player: dict) -> None:
    """
    Applies warrior class traits to the player

    :param player: dict, The player's state containing stats{

    :return: None, Updates the player's state with warrior class traits
    """

    player['c_class'] = 'Warrior'
    player['class_m'] = 2
    player['hp'] += 30
    player['hp_max'] = player['hp']
    player['mp'] = 30
    player['mp_max'] = player['mp']
    player['str'] = 12
    player['mag_str'] = 3
    player['defense'] = 1.5


def apply_wizard(player: dict) -> None:
    """
    Applies wizard class traits to the player

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state with wizard class traits
    """

    player['c_class'] = 'Wizard'
    player['class_m'] = 0.5
    player['hp'] -= 10
    player['hp_max'] = player['hp']
    player['mp'] += 30
    player['mp_max'] = player['mp']
    player['str'] -= 2
    player['mag_str'] += 3
    player['spell_book'].update({"Вогняна куля": 20})


def apply_merchant(player: dict) -> None:
    """
    Applies merchant class traits to the player

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state with merchant class traits
    """

    player['c_class'] = 'Merchant'
    player['class_m'] = 1
    player['hp_max'] = player['hp']
    player['mp'] += 30
    player['mp_max'] = player['mp']
    player['mag_str'] += 1
    player['gold'] += 100


def level_up(player: dict) -> None:
    """
    Checks if the player has enough experience to level up
    and applies the level up bonuses

    :param player: dict, The player's state containing stats

    :return: None, Updates the player's state if they level up
    """

    if player['exp'] >= player['cap_exp']:
        player['lvl'] += 1
        player['exp'] -= player['cap_exp']
        player['cap_exp'] = int(player['cap_exp'] * 1.1)
        player['hp_max'] += round(5 * player['class_m'])
        player['mp_max'] += round(5 * (1 / player['class_m']))
        player['str'] += round(2 * player['class_m'])
        player['mag_str'] += round(1 * (1 / player['class_m']))
        player['hp'] = player['hp_max']
        player['mp'] = player['mp_max']
        player['last_message'] = (f"{player['name']} перейшов "
            f"на новий курс {player['lvl']}!")


# === PLAYER MECHANICS ===


def get_input(prompt:str) -> str:
    """
    Handles user input and allow quitting the game by typing 'q' or 'quit'

    :param prompt: str, The prompt message to display to the user

    :return: str, The user's input in lowercase and stripped of whitespace
    """

    print(prompt)
    choice = input('>>> ').strip().lower()
    if choice in ('q', 'quit'):
        sys.exit('Виходжу. Прощавай!')

    return choice


def player_melee(player: dict, enemy: dict) -> None:
    """
    Melee attack action for the player against an enemy. 
    Calculates damage based on player's strength and enemy's defense,
    then reduces the enemy's HP accordingly.

    :param player: dict, The player's state containing stats
    :param enemy: dict, The enemy's state containing stats

    :return: None, Updates the enemy's HP based on the melee attack
    """
    min_str = 0
    if 'Залізний меч' in player['inventory']:
        min_str = 3

    dmg = random.randint(min_str, min_str +
        round(player['str'] / enemy['defense'] * player['crit_damage']))
    enemy['hp'] -= dmg
    player['last_message'] = f"{GREEN}Ви атакуєте {enemy['name']} на {dmg} шкоди!{NC}"
    if player['crit_damage'] == 2:
        player['last_message'] += f'\n{BOLD}{GREEN}КРИТИЧНЕ ПОПАДАННЯ{NC}'


def player_magic(player: dict, enemy: dict) -> None:
    """
    Magic attack action for the player against an enemy.
    Calculates damage based on player's magic strength and the spell's mana cost,
    then reduces the enemy's HP accordingly.

    :param player: dict, The player's state containing stats and spell book
    :param enemy: dict, The enemy's state containing stats

    :return: None, Updates the enemy's HP based on the magic attack
    """
    min_mag_str = 0
    if 'Cтаровонний посох' in player['inventory']:
        min_mag_str = 3
    if player['spell_book']:
        spells = list(player['spell_book'].keys())
        how_many_spells = len(player['spell_book'])
        print("Магічний фоліант:")
        for i in range(how_many_spells):
            print(f"{i+1}. {spells[i]}")

        spell_choice = get_input("Виберіть ваше заклинання:")
        spell_mana = 0

        if spell_choice.isdigit():
            index = int(spell_choice) - 1
            if 0 <= index < how_many_spells:
                spell_choice = spells[index]
                spell_mana = player['spell_book'][spell_choice]
            else:
                player['last_message'] = f"{RED}Йой, немає такого заклинання.{NC}"
                return None
        else:
            player['last_message'] = f"{RED}Йой, немає такого заклинання.{NC}"
            return None

        if player['mp'] >= spell_mana:
            player['mp'] -= spell_mana
            dmg = random.randint(min_mag_str, min_mag_str + round(player['mag_str']
                            * (spell_mana / 10) * player['crit_damage']))
            enemy['hp'] -= dmg
            player['last_message'] = (f"{GREEN}Ви творите {spell_choice} на "
                        f"{enemy['name']} та наносите {dmg} шкоди!{NC}")
            if player['crit_damage'] == 2:
                player['last_message'] += f'\n{BOLD}{GREEN}КРИТИЧНЕ ПОПАДАННЯ{NC}'
        else:
            player['last_message'] = f"{RED}Недостатньо мани для {spell_choice}!{NC}"
    else:
        player['last_message'] = f"{RED}Схоже у вас немає книги заклинань, " \
        f"на жаль, таке трапляється, треба зайти в крамничку{NC}"


def player_item(player: dict) -> None:
    """
    Allows the player to use an item from their inventory.

    :param player: dict, The player's state containing inventory and stats

    :return: None, Updates the player's state based on the item used
    """

    if player['estus'] > 0 or player['ashen'] > 0:
        print("Швидкий інвентар: \n")
        print("1. Фляга з Естусом \n2. Фляга з Попелом \n3. Назад\n")
        item_choice = get_input("Виберіть предмет:")

        if item_choice in ('1', 'естус'):
            if player['estus'] > 0:
                player['hp'] += 20
                if player['hp'] > player['hp_max']:
                    player['hp'] = player['hp_max']
                player['estus'] -= 1
                player['last_message'] = (f"{GREEN}Ви використали фляжку з Естусом "
                f"та відновили 20 здоров'я! Ви маєте ще {player['estus']} фляг з Естусом.{NC}")
            else:
                player['last_message'] = f"{GREEN}На жаль, у вас закінчились фляги з Естусом{NC}"

        elif item_choice in ('2', 'попіл'):
            if player['ashen'] > 0:
                player['mp'] += 20
                if player['mp'] > player['mp_max']:
                    player['mp'] = player['mp_max']
                player['ashen'] -= 1
                player['last_message'] = (f"{GREEN}Ви використали фляжку з Попелом "
                f"та відновили 20 мани! Ви маєте ще {player['ashen']} фляг з Попелом.{NC}")
            else:
                player['last_message'] = f"{RED}На жаль, у вас закінчились фляги з Попелом{NC}"

        elif item_choice in ('3', 'back'):
            pass

        else:
            player['last_message'] = "Щось я вас не зрозумів. Що ви хотіли дістати?"

    else:
        player['last_message'] = f"{RED}Ваші кишені пусті{NC}"


def move_player(player: dict, direction: str, game_map: dict) -> list:
    """
    Moves the player in the specified direction on the game map, if possible.
    Updates the player's location and the game map accordingly.

    :param player: dict, The player's state containing location
    :param direction: str, The direction to move back
    :param game_map: dict, The game map containing the layout

    :return: list, The updated player location
    """

    x, y = player['location']

    if direction in ('w', 'ц'):
        y -= 1
    elif direction in ('a', 'ф'):
        x -= 1
    elif direction in ('s', 'і'):
        y += 1
    elif direction in ('d', 'в'):
        x += 1
    else:
        return player['location']

    if x < 0 or x >= game_map['width'] or y < 0 or y >= game_map['height']:
        return player['location']

    game_map['map'][player['location'][1]][player['location'][0]] = '.'
    player['location'] = [x, y]
    game_map['map'][y][x] = f'{GREEN}P{NC}'

    return player['location']


def move_player_back(player: dict, direction: str, game_map: dict, restore_char: str = '') -> list:
    """
    Special case for town, dungeon, enemies where player leaves the encounter
    and needs to be moved back to the previous location.
    The function restores the character at the previous location
    and updates the player's location accordingly.

    :param player: dict, The player's state containing location
    :param direction: str, The direction to move back
    :param game_map: dict, The game map containing the layout
    :param restore_char: str, The character to restore at the previous location

    :return: list, The updated player location
    """

    x, y = player['location']
    game_map['map'][y][x] = restore_char

    if direction in ('w', 'ц'):
        y += 1
    elif direction in ('a', 'ф'):
        x += 1
    elif direction in ('s', 'і'):
        y -= 1
    elif direction in ('d', 'в'):
        x -= 1

    player['location'] = [x, y]
    game_map['map'][y][x] = f'{GREEN}P{NC}'

    return player['location']


def player_escape(player: dict, enemy: dict, move_dir: str, game_map: dict) -> bool:
    """
    Player attempts to escape from battle with an enemy.
    The success is determined by a random chance
    influenced by the player's level and the enemy's health.

    :param player: dict, The player's state containing stats
    :param enemy: dict, The enemy's state containing stats
    :param move_dir: str, The direction the player is trying to escape towards
    :param game_map: dict, The game map containing the layout

    :return: bool, True if the player successfully escapes, False otherwise
    """

    print('Ви пробуєте втекти')
    get_input('Нажміть Enter, щоб спробувати втекти...')
    escape_chance = random.randint(1, 100) + player['lvl'] - (enemy['hp'] / 4)

    if escape_chance >= 70:
        player['last_message'] = f"{GREEN}Ви успішно втекли!{NC}"

        enemy['hp'] = enemy['hp_max']
        enemy['mp'] = enemy['mp_max']

        if enemy.get('type') == 'boss':
            move_player_back(player, move_dir, game_map, restore_char='D')
        else:
            move_player_back(player, move_dir, game_map, restore_char=f'{RED}E{NC}')

        return True

    if escape_chance >= 50 :
        player['last_message'] = (f"{GREEN}Ви чудом втекли, "
        f"але поранились під час втечі{NC}")

        player['hp'] -= 10
        enemy['hp'] = enemy['hp_max']
        enemy['mp'] = enemy['mp_max']

        if enemy.get('type') == 'boss':
            move_player_back(player, move_dir, game_map, restore_char='D')
        else:
            move_player_back(player, move_dir, game_map, restore_char=f'{RED}E{NC}')
        return True

    player['last_message'] = f"{RED}Ви не змогли втекти і битва продовжується!{NC}"
    return False


# === ENEMY MECHANICS ===


def enemy_attack(enemy: dict, player: dict) -> None:
    """
    Enemy attack action against the player.
    Calculates damage based on enemy's strength and player's defense.

    :param enemy: dict, The enemy's state containing stats
    :param player: dict, The player's state containing stats

    :return: None, Updates the player's HP based on the enemy's attack
    """

    dmg = round(enemy['str'] / player['defense'])
    player['hp'] -= dmg
    enemy['last_message'] = f"{RED}{enemy['name']} атакував вас на {dmg} шкоди!{NC}"


def enemy_heal(enemy:dict, player:dict, need_mana:bool=False) -> None:
    """
    Enemy healing action. The enemy will restore mana if needed, or health if low.
    
    :param enemy: dict, The enemy's state containing stats
    :param player: dict, The player's state containing stats

    :return: None, Updates the enemy's HP or MP based on the healing action
    """

    if need_mana:
        healed = round(enemy['mp_max'] / 5)
        enemy['mp'] += healed
        enemy['last_message'] = f"{RED}{enemy['name']} відновив {healed} мани!{NC}"

    elif enemy['hp'] <= enemy['hp_max'] / 2 or enemy['hp'] <= enemy['hp_max'] - 50:
        healed = round(enemy['hp_max'] / 10)
        enemy['hp'] += healed
        enemy['last_message'] = f"{RED}{enemy['name']} відновив {healed} здоров'я!{NC}"

    else:
        enemy_attack(enemy, player)


def enemy_magic(enemy:dict, player:dict) -> None:
    """
    Enemy magic attack action against the player.
    Calculates damage based on enemy's magic strength and the spell's mana cost.

    :param enemy: dict, The enemy's state containing stats and spell book
    :param player: dict, The player's state containing stats

    :return: None, Updates the player's HP based on the magic attack
    """

    if enemy['spell_book']:
        spells = list(enemy['spell_book'].keys())
        spell_choice = random.choice(spells)
        spell_mana = enemy['spell_book'][spell_choice]

        if enemy['mp'] >= spell_mana:
            enemy['mp'] -= spell_mana
            dmg = 5 + round(enemy['mag_str'] * (spell_mana / 10))
            player['hp'] -= dmg
            enemy['last_message'] = (f"{RED}{enemy['name']} використав {spell_choice} "
                                     f"на вас та наніс {dmg} шкоди!{NC}")

        else:
            enemy_heal(enemy, player, need_mana=True)

    else:
        enemy_attack(enemy, player)


# === TOWN LOGIC ===


def town_menu(state: dict, entry_direction:str=None) -> None:
    """
    Displays the town menu and handles user choices for interacting with the town.

    :param state: dict, The game state containing player, town, and other relevant information
    :param entry_direction: str, The direction from which the player entered the town (optional)
    
    :return: None, Updates the game state based on the player's choices in the town
    """

    print("Вітаю на кампусі! Стоп, схоже ви найшли УКУ в цьому таємничому вимірі!\n"
          "Щоб ви воліли б зробити?")

    while True:
        print(f"{state['player']['name']} на {state['player']['lvl']} курсі\n"
            f"Здоров'я: {state['player']['hp']}/{state['player']['hp_max']} "
            f"Мана: {state['player']['mp']}/{state['player']['mp_max']}\n"
            f"Гривень: {state['player']['gold']}")
        print('-' * 30)
        print("1. Піти у корчму\n2. Піти у крамницю\n3. Залишити територію кампусу\n")
        choice = get_input("Ваш вибір:")

        if choice in ('1', 'корчма'):
            town_inn(state)
            state['player']['entry_direction'] = entry_direction

        elif choice in ('2') or choice.startswith('крам'):
            shop_menu(state)
            state['player']['entry_direction'] = entry_direction

        elif choice in ('3', 'залишити'):
            state['player']['last_message'] = "Ви покидаєте кампус."
            if entry_direction is None:
                state['player']['entry_direction'] = entry_direction
            move_player_back(state['player'], entry_direction, state['game_map'], restore_char='T')
            break
        else:
            print("Повторіть ще раз, я вас не зрозумів.")


def town_inn(state:dict) -> None:
    """
    Handles the inn interaction within the town.

    :param state: dict, The game state containing player and town information
    :return: None
    """

    print('''Вітаю в корчмі "Срібне вогнище"! Що ви хочете зробити?''')

    while True:
        print(f"{state['player']['name']} на {state['player']['lvl']} курсі\n"
                    f"Здоров'я: {state['player']['hp']}/{state['player']['hp_max']} "
                    f"Мана: {state['player']['mp']}/{state['player']['mp_max']}\n"
                    f"Гривень: {state['player']['gold']}")
        print('-' * 30)
        print("1. Вийняти кімнату за 20 гривень " \
        "\n2. Поговорити з господарем\n3. Вийти назад на головну площу")

        choice = get_input("Ваш вибір:")

        if choice in ('1', 'вийняти', 'кімната'):
            if state['player']['gold'] >= 20:
                state['player']['gold'] -= 20
                print(f"{RED}Ви орендуєте кімнату за 20 гривень " \
                f"та дуже добре відпочиваєте,\nпрокидаєтесь ви дуже виспані та щасливі\n{NC}")
                state['player']['hp'] = state['player']['hp_max']
                state['player']['mp'] = state['player']['mp_max']
                print("Ваше здоров'я та мана повністю відновилась!\n")

            else:
                print(f"{RED}Ви занадто бідні, " \
                "щоб дозволити собі комфортний відпочинок,\n" \
                f"тож ви повертаєтесь до головної зали\n{NC}")

            town_inn(state)

            break

        if choice in ('2', 'поговорити', 'господар'):
            town_talk_bartender(state)
            break

        if choice in ('3', 'назад', 'вийти', 'площа'):
            break

        print('''"Що ви собі під ніс там бурмочите?
          Голосніше говоріть." змучено звертається до вас господар корми''')


def town_talk_bartender(state: dict) -> None:
    """
    Handles the interaction with the bartender in the inn.

    :param state: dict, The game state containing player and town information

    :return: None, Updates the game state based on the player's conversation with the bartender
    """

    print('\n"Вітаю вас у корчмі!Чи я можу запропонувати Вам щось випити? Пиво, ель?"')

    while True:
        print('1. Пиво\n2. Ель\n3. Спитати про місцину\n4. "Нічого, дякую"')

        choice = get_input("Ваш вибір:")

        if choice in ('1', 'пиво'):
            if state['player']['mp'] - state['player']['mp_max'] < 50:
                state['player']['mp'] += 10
                print(f"{GREEN}Господар корчми приносить вам холоднезне пиво.\n" \
                f"Ви робите ковточок та почуваєтесь краще.{NC}\n")
            else:
                print(f'{RED}Вам стає погано, схоже ви перепили\n' \
                f'Не варто було зловживати безкоштовною випивкою{NC}')
                state['player']['mp'] = state['player']['mp_max'] // 5

        elif choice in ('2', 'ель'):
            if state['player']['hp'] - state['player']['hp_max'] < 50:
                state['player']['hp'] += 10
                print(f"{GREEN}Господар корчми приносить вам міцний ель.\n" \
                f"Ви опорожнюєте пінту та відчуваєте як тепло розходиться по тілу.{NC}\n")
            else:
                print(f'{GREEN}Вам стає погано, схоже ви перепили\n' \
                f'Не варто було зловживати безкоштовною випивкою{NC}')
                state['player']['hp'] = state['player']['hp_max'] // 5

        elif choice in ('3', 'місцина'):
            print('Хазяїн корчми розказує вам про страшенне підземелля\n'
            'з якого час від часу доносяться жахливі завивання.\n'
            '"ЧООООООМУ ВОНО НЕ ПРАЦЮЄ, ЗА ЩОООООООО" найбільш пристойне серед них\n'
            'Він говорить, що всередині підземелля, живе страшний монстр,\n' 
            'який час-від-час телепортує до цього виміру різні речі, що робить клопіт місцевим.\n\n'
            'Його слова наштовхують на можливе рішення вашої проблеми.\n'
            f'{BOLD}Ймовірно, якщо вбити чудовисько, то УКУ вернеться у ваш вимір.{NC}\n')

        elif choice in ('4', 'нічого', 'дякую'):
            print("Володар заклажу киває та продовжує " \
            "протирати стару-задрипану поверхню барної стійки.")
            break
        else:
            print('"Скажіть голосніше, а то я з часом почав недочувати"' \
            ' говорить дідуган за стійкою')

    print('"Повертайтесь, якщо знадобляться ' \
    'припаси чи потребуватимете відпочинку"\nговорить він вам у спину.')
    get_input('Нажміть Enter, щоб вийти')


def shop_menu(state:dict, ask_continue:bool=False) -> None:
    """
    Displays the shop menu and handles player interactions.

    :param state: dict, The game state containing player information
    :param ask_continue: bool, Whether to ask the player if they want to continue shopping
    
    :return: None, Updates the game state based on the player's actions in the shop
    """

    if ask_continue:
        while True:
            answer = get_input("Ви хочете далі скуплятись?\n1. Так\n2. Ні")
            if answer in ('1'):
                return shop_menu(state, False)
            if answer in ('2'):
                break


    shop_catalog = {
        "1": {"name": "Фляга з Естусом", "price": 15,},
        "2": {"name": "Фляга з Попелом", "price": 15},
        '3': {"name": "Залізний меч", "price": 30},
        '4': {"name": "Cтаровинний посох", "price": 30},
        '5': {'name': 'Заклинання: Блискавки', 'price': 50}
    }

    if not ask_continue:
        print('''Вітаю вас у крамниці "Співаюче ковадло"! Що ви хочете зробити?''')

        while True:
            print("1. Купити прeдмети\n2. Продати предмети\n3. Повернутись в містечко")
            choice = get_input("Ваш вибір:")
            if choice in  ('1', 'купити'):
                shop_buy_sell(state, shop_catalog, buying=True)
                break

            if choice in ('2', 'продати'):
                shop_buy_sell(state, shop_catalog, buying=False)
                break

            if choice in ('3', 'назад'):
                break

            print('Сивий дворф у розквіті сил глянув на вас ' \
            'ніби ви щось сказали,\nале зразу повернувся до ковання виробів')


def shop_buy_sell(state:dict, catalog:dict, buying:bool) -> None:
    """
    Handles the buying and selling of items in the shop.

    :param state: dict, The game state containing player information
    :param catalog: dict, The shop's catalog of items available for purchase or sale
    :param buying: bool, True if the player is buying items, False if selling

    """
    while True:
        for key, item in catalog.items():
            if not buying and item['name'] in ('Заклинання: Блискавки'):
                continue
            num = int(key)
            print(f"{key}. {item['name']} - {item['price']} гривень")
        print(f'{num+1}. Вийти')
        choice = get_input("Ваш вибір:")

        if buying:
            pass
        else:
            catalog.popitem()

        if choice in catalog and choice != f'{num+1}':
            print()
            item = catalog[choice]
            if buying:
                if state['player']['gold'] >= item["price"]:
                    state['player']['gold'] -= item["price"]
                    if item["name"] == "Фляга з Естусом":
                        state['player']['estus'] += 1
                    elif item["name"] == "Фляга з Попелом":
                        state['player']['ashen'] += 1
                    elif item['name'] == 'Залізний меч':
                        state['player']['inventory'].add('Залізний меч')
                    elif item['name'] == 'Старовинний посох':
                        state['player']['inventory'].add('Старовинний посох')
                    elif item['name'] == 'Заклинання: Блискавки':
                        state['player']['spell_book'].update({'Блискавка': 100})
                        print('Ви вивчили нове заклинання тепер воно у вашій книжці')
                        print('Цей предмет ви не можете продати')
                    print(f"{GREEN}Ви купили {item['name']}!\n{NC}")
                else:
                    print(f"{RED}Недостатньо грошей, щоб купити {item['name']}.\n")
                shop_menu(state, ask_continue=True)
            else:
                if item["name"] == "Фляга з Естусом" and state['player']['estus'] > 0:
                    state['player']['gold'] += item["price"]//2
                    state['player']['estus'] -= 1
                    print(f"{GREEN}Ви продали {item['name']}!\n{NC}")
                elif item["name"] == "Фляга з Попелом" and state['player']['ashen'] > 0:
                    state['player']['gold'] += item["price"]//2
                    state['player']['ashen'] -= 1
                    print(f"{GREEN}Ви продали {item['name']}!\n{NC}")
                elif (item['name'] == 'Старовинний посох'
                and 'Старовинний посох' in state['player']['inventory']):
                    state['player']['gold'] += item["price"]//2
                    state['player']['inventory'].remove('Старовинний посох')
                    print(f"{GREEN}Ви продали {item['name']}!{NC}\n")
                elif (item['name'] == 'Залізний меч'
                and 'Залізний меч' in state['player']['inventory']):
                    state['player']['gold'] += item["price"]//2
                    state['player']['inventory'].remove('Залізний меч')
                    print(f"{RED}Ви продали {item['name']}!{NC}")
                else:
                    print(f"{RED}Ви не маєте {item['name']}, щоб продати.{NC}\n")
                shop_menu(state, ask_continue=True)
            break
        if choice == f'{num+1}':
            break
        print('"Час - гроші, не марнуйте його, вибирайте, або забирайтесь звідси"\n' \
        'Говорить вам дворф за прилавком\n')


# === DUNGEON LOGIC ===


def dungeon_menu(state:dict, entry_direction:str=None) -> None:
    """
    Displays the dungeon menu and handles player interactions within the dungeon.

    :param state: dict, The game state containing player and dungeon information
    :param entry_direction: str, The direction from which the player entered the dungeon (optional

    :return: None, Updates the game state based on the player's actions in the dungeon
    """

    print("Це підземелля, ні, це ІТ-спейс, схоже УКУ не лише перекинуло у цей вимір,\n" \
    "але ще й розкидало по ньому")
    while True:
        print("1. Повернутись назад\n2. Йти далі")
        choice = get_input("Ваш вибір:")
        if choice in ('1', 'назад', 'карта'):
            state['player']['last_message'] = ("Ви покидаєте підземелля, "
            "у спину вам доносяться жахливі звуки,\n" \
            "ви налякано, з усіх сил втікаєте на білий світ, " \
            "але падаєте через цилідричного\nмонстра, " \
            "лише продовжуючи повзти, ви змогли втікти з цього жахливого місця.")
            move_player_back(state['player'], entry_direction, state['game_map'], restore_char='D')
            break

        if choice in ('2', 'далі'):
            if not state['player']['boss_item']:
                battle(state, state['dungeon']['boss'], entry_direction)
                if state['player']['boss_item']:
                    sys.exit(f'Як тільки стихає {state['boss']['name']} і з вуст цієї істоти '
                             'більше не чутно навіть подиху,\nоточення навколо вас міняється. '
                             'Вийшовши з підземелля, ви бачите знайому місцину навколо,\n' 
                             'Стрийський парк, Податкову, Львів... Cхоже ви змогли.\n\n'
                             'Ви повернули УКУ на його законне місце у нашому світі. ВІТАЮ!!!')
            break

        print("Напевно через стукіт ваших зубів, я вас не зрозумів, давайте спробуємо ще раз")


# === MAP LOGIC ===


def get_random_empty_location(game_map:dict) -> tuple:
    """
    Finds a random empty location on the game map that is not occupied
    by the player or other entities.
    The function ensures that the location is valid and not the player's starting position.
    
    :param game_map: dict, The game map containing the layout and dimensions

    :return: tuple, (x, y) coordinates of a random empty location on the map

    """

    while True:
        x = random.randint(0, game_map['width'] - 1)
        y = random.randint(0, game_map['height'] - 1)
        if game_map['map'][y][x] == '.' and (x, y) != (1, 1):
            return x, y


def place_enemies(game_map:dict, enemies:list) -> None:
    """
    Places enemies on the game map at random empty locations.
    Each enemy's location is updated in the game map and the enemy's state.

    :param game_map: dict, The game map containing the layout and dimensions
    :param enemies: list, A list of enemy dictionaries to be placed on the map

    :return: None, Updates the game map and enemy states with their new locations
    """

    for enemy in enemies:
        enemy['location'] = list(get_random_empty_location(game_map))
        game_map['map'][enemy['location'][1]][enemy['location'][0]] = f'{RED}E{NC}'


def display_map(game_map:dict) -> None:
    """
    Displays the current state of the game map in the console.
    Each row of the map is printed, with characters
    representing different entities (e.g., player, enemies, town, dungeon).

    :param game_map: dict, The game map containing the layout and dimensions

    :return: None, Prints the game map to the console
    """

    for row in game_map['map']:
        print(' '.join(row))


def clear_screen() -> None:
    """
    Identifies system and clears the screen using right command for each system accordingly

    :return: None, Clears console 
    """

    os.system('cls' if os.name == 'nt' else 'clear')


# === CORE GAME LOOP & BATTLE ===


def battle(state: dict, enemy: dict, direction: str, need_mana: bool = False) -> None:
    """
    Handles the battle sequence between the player and an enemy.
    The player can choose to attack, use magic, use an item, or attempt to run away.
    The battle continues until either the player(or run away) or the enemy is defeated.

    :param state: dict, The game state containing player and enemy information
    :param enemy: dict, The enemy's state containing stats and information
    :param direction: str, The direction from which the player entered the battle (used for
    moving back if the player escapes)
    :param need_mana: bool, Whether the enemy needs to restore mana during the battle

    :return: None, Updates the game state based on the battle outcome
    """

    player = state['player']
    enemy['hp_max'] = enemy['hp']
    enemy['mp_max'] = enemy['mp']

    print(f"{BOLD}Ви натрапили на {enemy.get('name', 'Ворог')}!\nБитва починається!\n{NC}")

    while player['hp'] > 0 and enemy['hp'] > 0:
        print(f"{player['name']} Здоров'я: {player['hp']}/{player['hp_max']} | "
            f"Mана: {player['mp']}/{player['mp_max']}")
        print(f"{enemy.get('name', 'Ворог')} Здоров'я: {enemy['hp']}/{enemy['hp_max']}\n")

        if player['last_message']:
            print(f'{player['last_message']}')
        if enemy['last_message']:
            print(f'{enemy['last_message']}\n')
        print("Дія:\n1. Атака\n2. Магія\n3. Предмети\n4. Втеча\n")

        player['last_message'] = ''
        enemy['last_message'] = ''

        action = get_input("Виберіть дію:")
        dice = random.randint(1, 20)
        if dice == 20:
            player['crit_damage'] = 2

        if dice == 1:
            player['last_message'] = f'{RED}ОЙ-ОЙ-ОЙ, ви заплутались в своїх ногах і впали{NC}'
            player['hp'] -= 10
        else:
            if action in ('1', 'атака'):
                player_melee(player, enemy)

            elif action in ('2', 'магія'):
                player_magic(player, enemy)

            elif action in ('3', 'предмети'):
                player_item(player)

            elif action in ('4', 'втеча'):
                if player_escape(player, enemy, direction, state['game_map']):
                    break
            else:
                player['last_message'] = (f"{RED}Не варто зараз гаяти час. "
                f"А то час згаїть вас, обирайте дію{NC}")

        player['crit_damage'] = 1
        print()
        if enemy['hp'] > 0:
            # Use functools.partial to prefill func
            # Without it, will get TypeError: NoneType object is not callable
            enemy_actions = [
                partial(enemy_attack, enemy, player),
                partial(enemy_magic, enemy, player),
                partial(enemy_heal, enemy, player, need_mana)
            ]

            random.choice(enemy_actions)()

        clear_screen()

    if player['hp'] <= 0:
        sys.exit(f"{RED}Вас переміг {enemy['name']}.\n"
                 f"На жаль, УКУ назавжди стало частиною Арілонгу, як і ви{NC}")

    elif enemy['hp'] <= 0:
        print(f"{GREEN}Ви перемогли {enemy.get('name', 'Enemy')}! "
        f"Ви отримали {enemy.get('exp', 0)} очків досвіду та {enemy.get('gold', 0)} гривень.{NC}")

        player['last_message']= ''
        player['exp'] += enemy.get('exp', 0)
        player['gold'] += enemy.get('gold', 0)

        if enemy in state['enemies']:
            state['enemies'].remove(enemy)
            get_input('Нажміть Enter, щоб продовжити')
        if enemy == state['boss']:
            player['boss_item'] = True


def start_new_game(state:dict) -> dict:
    """
    Initializes a new game by setting up the player's race, name, and class.

    :param state: dict, The game state containing player and other relevant information

    :return: dict, The updated game state after initializing the new game
    """

    clear_screen()

    player = state['player']

    print('Проходження через портал якось змінило ваше тіло,' \
    '\nпідійшовши до потічка поблизу ' \
    'ви розумієте, що ви тепер:\n')

    while not player['race']:
        print('1.Ельф\n2.Людина\n3.Дворф')

        race_choice = get_input('Ваш вибір:')
        if race_choice in ['1', 'ельф']:
            apply_elf(player)
        elif race_choice in ['2', 'людина']:
            apply_human(player)
        elif race_choice in ['3', 'дворф']:
            apply_dwarf(player)
        else:
            player['race'] = ""
            print('Навіть я про таких істот не чув. Давайте ближче до правди\n ')

    clear_screen()

    while not player['name']:
        player['name'] = get_input("Ви пробуєте пригадати своє ім'я...")
        print("Гей, назовіться, не гоже бути без імені")

    clear_screen()

    print('З неймовірним мігренем ви пробуєте пригадати, хто ж ви такі?\n\n' \
            'Через хвилину, що здалась вам як години, ви розумієте, ' \
            'що раніше тіло,\nв якому ви зараз, ' \
            'мало свою свідомість, отже і навички, але ж які?\n')

    while not player['c_class']:
        print('1.Торговця\n2.Воїна\n3.Мага')

        class_choice = get_input('Ваш вибір:')

        if class_choice in ['1', 'торговця']:
            apply_merchant(player)

        elif class_choice in ['2', 'воїна']:
            apply_warrior(player)

        elif class_choice in ['3', 'мага']:
            apply_wizard(player)

        else:
            player['c_class'] = ""
            print('Та немає тут такого обирайте, що дають\n')

    return state


def main_menu(state:dict) -> dict:
    """
    Displays the main menu and handles user choices.

    :param state: dict, The game state

    :return: dict, The updated game state based on user choice
    """

    # Just in case if server will be on Windows
    if sys.stdout.encoding != 'utf-8':
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')

    print(f"""\nЦе текстова рольова гра, де ваше завдання полягає у порятунку
кампусу УКУ від виміру Арілонг.\n\nДля переміщення по глобальній карті використовуйте клавіші W
для руху вгору, A для руху вліво, S для руху вниз та D для руху вправо, 
після чого натискайте Enter.\n
Карта виглядає як сітка, де порожні місця позначені крапками, літера P
позначає вашого персонажа, T це містечко, D це підземелля з фінальним
босом, а E це вороги.\n
Щоб робити вибір у діалогах чи меню, вводьте відповідну цифру варіанту. 
Для виходу з гри у будь-який момент введіть q або quit. \n
У корчмі можна орендувати кімнату за 20 гривень для повного відновлення здоров'я та
мани, або ж випити пиво чи ель, які дають невеликі бонуси до характеристик. 
У крамниці можна купувати та продавати фляги з Естусом і Попелом, 
що відновлюють здоров'я та ману відповідно, по 15 гривень за штуку.
Також в крамниці можна купити посилення для битви.\n
Перед походом у підземелля до фінального боса рекомендується добре
прокачати персонажа та запастися цілющими флягами.\n
{BOLD}Повбивайте ворогів, купіть спорядження та переможіть монстра підземелля\n
Приємної гри{NC}
""")

    get_input('Нажміть Enter, щоб перейти до гри.')

    clear_screen()

    print('\nХолодний листопадовий вечір, ви тільки-тільки повернулись з навчання додому.\n\n' \
    "Зробивши собі улюблений теплий напій, ви сідаєте за\nкомп'ютер " \
    "і бачите на уківській пошті лист.\n\n"
    "Зітхаючи та приговорюючи, що у вас ні секунди покою, ви читаєте його")

    get_input('Нажміть Enter, щоб прочитати лист')

    message = f"""\n{BOLD}УКРАЇНСЬКИЙ КАТОЛИЦЬКИЙ УНІВЕРСИТЕТ
    Екстрений штаб із питань просторово-часових аномалій та релокації{NC}

    
    {BOLD}Вих. №:{NC} 01-43/Б
    {BOLD}Тема:{NC} Оновлені дані щодо рятувальної місії та офіційний запит
    на Вашу участь

    {BOLD}Шановний/а кандидате!{NC}

    Цим листом офіційно повідомляємо Вас про те, що внаслідок 
    непередбачуваної технічної ситуації під час проведення експерименту 
    в одній із лабораторій Українського католицького університету відбулося 
    просторове зміщення. Увесь університетський кампус було 
    дематеріалізовано та перенесено до альтернативного виміру, 
    класифікованого як «Арілонг».

    Згідно з останніми телеметричними даними, що надійшли до нашого штабу, 
    умови в новому середовищі є екстремальними. Вимір Арілонг перебуває 
    на стадії соціально-технічного розвитку, що відповідає земному 
    Середньовіччю. Крім того, повідомляємо про критичний рівень 
    біологічної небезпеки: місцева фауна ідентифікована як вкрай ворожа 
    та агресивна.

    Незважаючи на ці обставини, ситуація залишається контрольованою. 
    Робоча група у складі студентів та викладачів, які на момент інциденту 
    перебували поза межами студентського містечка, успішно спроєктувала 
    стабілізований міжвимірний портал. Поточні потужності системи дозволяють 
    відправити на територію виміру Арілонг лише одну уповноважену особу.
    Наголошуємо на порушенні стандартів охорони праці під час переходу: 
    транзит через міжвимірний простір несе значні ризики. Існує висока 
    ймовірність того, що після телепортації Ваше тіло зазнає суттєвих 
    (або ж не дуже суттєвих) фізичних чи структурних трансформацій.

    Враховуючи вищезазначені ускладнення, а також агресивне середньовічне 
    середовище Арілонгу, Адміністрація УКУ повторно звертається до Вас 
    із запитом: чи надаєте Ви добровільну згоду очолити експедицію 
    та допомогти повернути будівлю Трапезної, а також усі прилеглі 
    землі студмістечка, у наш просторово-часовий континуум?

    Просимо підтвердити Вашу готовність у найкоротші терміни, оскільки 
    портал працює на резервних генераторах.

    З повагою,

    {BOLD}Оперативний штаб порятунку кампусу
    Адміністрація Українського католицького університету (в екзилі){NC}"""

    print(message)

    while True:
        print('\n1. Погодитись\n2. "Моя хата з краю, хай самі розбираються"')
        choice = get_input('Ваш вибір:')

        if choice in ['1', 'почати']:
            return start_new_game(state)
        if choice in ['2']:
            sys.exit(f'\n{RED}Буквально за декілька хвилин вам приходить відповідь:\n'
                     '"Нам дуже прикро, що Ви вирішили не погоджуватись".\n' \
                     'Проте вам все рівно, бо ви впевнені, що вони найдуть когось іншого.\n\n' \
                     'Пройшов тиждень, місяць, рік, але на місці Козельницької 2\n'
                     'все ще знаходиться велетенський котлован.\n\n' \
                     f'З часом ця вирва стала одним із багатьох туристичних місць Львова{NC}\n'
                     'Напевно вона тут назавжди, цікаво чи змінились б історія,\n' \
                     'якщо б ви погодились того холодного листопадового вечора?')

        print("Це так?! Будь ласка, відпишіть зрозуміліше.")


def run_game_loop(state:dict) -> dict:
    """
    Runs the main game loop, handling player movement, encounters, and interactions.
    
    :param state: dict, The game state containing player, map, and other relevant information

    :return: dict, The updated game state after the game loop execution
    """

    game_map = state['game_map']
    player = state['player']
    wrong_move = False
    direction = ''

    tx, ty = game_map['town_location']
    game_map['map'][ty][tx] = 'T'

    dx, dy = game_map['dungeon_location']
    game_map['map'][dy][dx] = 'D'

    px, py = player['location']
    game_map['map'][py][px] = f'{GREEN}P{NC}'


    place_enemies(game_map, state['enemies'])


    print('"Напевно Вам вартувало б, сходити в місто, в корчму, '
    'відпочити та дізнатись більше\nпро цей світ" говорить вам старий чоловяга, що проходив мимо')

    get_input('Натисніть Enter, щоб зрозуміти, що він говорить')

    while True:
        clear_screen()

        print(f"{player['name']} на {player['lvl']} курсі\n"
              f"Здоров'я: {player['hp']}/{player['hp_max']} "
              f"Мана: {player['mp']}/{player['mp_max']}")

        print("-" * 30)

        if player['last_message']:
            print(player['last_message'])
            print("-" * 30)
            player['last_message'] = ""

        level_up(player)

        if wrong_move:
            if direction in ('w', 'ц', 'a', 's', 'd', 'ф', 'і', 'в'):
                print('Не ходіть туди, там живуть дракони')
            else:
                print('Ну то не серйозно, напишіть правильний напрямок')
            wrong_move = False

        display_map(game_map)
        result = get_input("Пересувайтесь на W/A/S/D:")

        direction = result
        location = player['location']

        new_location = move_player(player, direction, game_map)
        if new_location == location:
            wrong_move = True

        if new_location == list(game_map['town_location']):
            town_menu(state, direction)
        elif new_location == list(game_map['dungeon_location']):
            dungeon_menu(state, direction)
        else:
            for enemy in state['enemies']:
                if enemy['location'] == new_location:
                    battle(state, enemy, direction)
                    break

        if player['hp'] <= 0:
            sys.exit(f'{RED}На жаль, УКУ назавжди стало частиною Арілонгу, як і ви')


def main() -> None:
    """
    Main function to start the game.
    Initializes the game state and starts the main game loop.
    """

    initial_game_map = create_game_map(7, 7)

    initial_player = create_player()
    initial_boss = create_boss("Розлючений немертвий", hp=200, mp=300, defense=1, strength=1,
                                mag_str=3, spell_book={"Вогняна куля": 20,
                                                       "Блискавка": 100,
                                                       "Бурління лави": 50})

    initial_enemies = [
        create_enemy("Бронелом Костян", hp=35, mp=0, defense=2, strength=3, mag_strength=0,
                    spell_book={}, location=(0, 0)),
        create_enemy("Ігніс Попелястий", hp=15, mp=40, defense=0.5, strength=1, mag_strength=4,
                    spell_book={'Вогняна куля': 20}, location=(0, 0)),
        create_enemy("Соціус Лінивий", hp=1, mp=1, defense=0.1, strength=0, mag_strength=0,
                    spell_book={}, location=(0, 0)),
        create_enemy("Лицар Порчі", hp=100, mp=50, defense=2, strength=4, mag_strength=1,
                    spell_book={'Порча': 20}, location=(0, 0)),
        create_enemy("Cпустошений студент", hp=20, mp=20, defense=0.5, strength=1, mag_strength=1,
                    spell_book={'Депресія': 20}, location=(0, 0)),
    ]

    initial_town = create_town(initial_game_map['town_location'])
    initial_dungeon = create_dungeon(initial_game_map['dungeon_location'], initial_boss)

    game_state = {
        'player': initial_player,
        'enemies': initial_enemies,
        'boss': initial_boss,
        'game_map': initial_game_map,
        'town': initial_town,
        'dungeon': initial_dungeon,
    }

    game_state = main_menu(game_state)

    while True:
        run_game_loop(game_state)


# === MAIN EXECUTION ===
if __name__ == "__main__":
    main()
