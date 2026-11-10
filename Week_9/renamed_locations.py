"""
Lab week 9
Decommunisation
"""

def replace_prefix(name:str) -> str:
    """
    Cleans prefixes and shortens them

    :param name: str, A name of settlement

    :return: str, Cleaned name for settlement

    >>> replace_prefix('селище Петрівське')
    'с-ще Петрівське'
    >>> replace_prefix('село Ленінка')
    'с.Ленінка'
    """
    name = name.strip()
    if name.startswith("селище міського типу "):
        return name.replace("селище міського типу ", "смт ", 1)
    if name.startswith("селище "):
        return name.replace("селище ", "с-ще ", 1)
    if name.startswith("село "):
        return name.replace("село ", "с.", 1)
    if name.startswith("місто "):
        return name.replace("місто ", "м.", 1)
    return name


def read_file(pathfile: str) -> dict[tuple, str]:
    """
    Reads file and formats in dictionary for writing in csv

    :param pathfile: str, A path to to file to read

    :return: dict[tuple, str], A dictionary where tuple with oblast and disctrict is key 
    and value is new name for settlement 

    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
    ... encoding='utf-8') as tmp:
    ...     _ = tmp.write("Відповідно до пункту 29 частини першої статті 85\\n \
    10) у Львівській області:\\n \
    село Андріївка Буського району на село Мармузовичі;\\n \
    село Максимівка Терлівської сільської ради Старосамбірського району на село Лібухова;\\n \
    станом на 16.10.2023")
    >>> read_file(tmp.name)
    {('Львівська область', 'Буський район', 'с.Андріївка'): 'с.Мармузовичі', \
('Львівська область', 'Старосамбірський район', \
'с.Максимівка Терлівської сільської ради'): 'с.Лібухова'}
    >>> os.remove(tmp.name)

    """
    info = {}
    current_district = ''
    current_oblast = ''

    with open(pathfile, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    for line in data:
        line = line.strip()
        if not line:
            continue

        parts = line.rstrip(";., \t").split(' на ', 1)
        if len(parts) != 2:
            line = line.rstrip(":")
            if ")" in line[:5]:
                line = line.split(")", 1)[1].strip()

            lower_line = line.lower()
            if lower_line.startswith(("у ", "в ")):
                line = line[2:].strip()
                lower_line = line.lower()

            if "област" in lower_line:
                current_oblast = line.replace(
                    "ій області", "а область").replace("області", "область").strip()
                current_district = ""
            elif "район" in lower_line:
                current_district = line.replace(
                    "ому районі", "ий район").replace("ого району", "ий район").strip()
            elif "рад" in lower_line:
                current_district = line.replace(
                    "ій раді", "а рада").replace("ої ради", "а рада").strip()
            continue



        old, new = parts[0].strip(), parts[1].strip()
        old_parts = old.split()
        if not (old.startswith("село ") or old.startswith("селище ") or old.startswith("місто ")):
            continue

        entry_district = current_district

        if len(old_parts) >= 2 and old_parts[-1].startswith(("району", "район")):
            entry_district = " ".join(old_parts[-2:]).replace(
                "ього району", "ій район").replace("ого району", "ий район")
            old_parts = old_parts[:-2]
        elif len(old_parts) >= 3 and old_parts[-1].startswith(("ради", "рад")):
            entry_district = " ".join(old_parts[-3:]).replace(
                "ьої", "я").replace("ої", "а").replace("ради", "рада")
            old_parts = old_parts[:-3]

        old_name = replace_prefix(' '.join(old_parts))
        if old_name:
            info[(current_oblast, entry_district, old_name)] = replace_prefix(new)

    return info


def write_csv_file(info:dict, pathfile:str) -> None:
    """
    Writes to csv file dictionary with new names of settlements and their locations

    :param info: dict, A dictionary where tuple with oblast and disctrict is key 
    and value is new name for settlement 
    :param pathfile: str, A path to to file to read

    :return: None, just writes dict to csv file

    >>> import tempfile, os
    >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as out:
    ...     pass
    >>> write_csv_file({('Вінницька область', 'Барський район', 'c.Червоне'): 'c.Грабівці', 
    ...              ('Вінницька область', 'Вінницький район', 'c.Красне'): 'c.Махнівка'}, out.name)
    >>> with open(out.name, encoding='utf-8') as file:
    ...     print(file.read(), end='')
    regionname,areaname,oldname,newname
    Вінницька область,Барський район,c.Червоне,c.Грабівці
    Вінницька область,Вінницький район,c.Красне,c.Махнівка
    >>> os.remove(out.name)
    """
    with open(pathfile, 'w', encoding='utf-8') as file:
        file.write('regionname,areaname,oldname,newname\n')
        lines = []
        for (region, area, old), new in info.items():
            lines.append(f"{region},{area},{old},{new}")
        file.write('\n'.join(lines))


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
