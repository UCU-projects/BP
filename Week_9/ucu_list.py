"""
Діагностика зору пацієнтів: зчитування результатів тестів, пошук і позначення
помилок, діагноз і запис звіту у файл.
"""

DISEASES_DICT = {
    "astigmatism": {("A", "B")},
    "cataracts": {("F", "D"), ("A", "B")},
    "glaucoma": {("Z", "K")},
}

# Над кожною функцією вказано бали за функціональність:
# разом 6.4 бала, ще до 1.6 бала дає якість коду (pylint).


# 0.8 бала
def read_file(filepath: str) -> list[list[str]]:
    """
    Зчитує результати тестів пацієнтів із файлу.

    Кожен непорожній рядок має вигляд
        ПРІЗВИЩЕ ІМ'Я: ВІДПОВІДІ_ПАЦІЄНТА|ПРАВИЛЬНІ_ВІДПОВІДІ
    Пацієнт записаний як прізвище та ім'я через один пробіл, після
    двокрапки — рівно один пробіл. Відповіді — великі літери без пробілів.
    Кількість питань у різних пацієнтів може бути різною, але в одного
    пацієнта відповідей завжди стільки ж, скільки правильних відповідей.
    Порожні рядки треба пропускати.

    Аргументи:
        filepath: шлях до вхідного файлу

    Повертає:
        list[list[str]]: [пацієнт, відповіді_пацієнта, правильні_відповіді]
        для кожного рядка в порядку файлу

    Приклад:
        >>> import tempfile, os
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False,
        ...                                  encoding='utf-8') as tmp:
        ...     _ = tmp.write("Franko Ivan: ABCD|ABDF\\n\\nKosach Olena: AA|AA\\n")
        >>> read_file(tmp.name)
        [['Franko Ivan', 'ABCD', 'ABDF'], ['Kosach Olena', 'AA', 'AA']]
        >>> os.remove(tmp.name)
    """
    with open(filepath, 'r', encoding='utf-8') as file:
        data = file.read().splitlines()

    patients_list = []
    for line in data:
        if line:
            colon_place = line.find(':')
            name = line[:colon_place]
            line = line[colon_place+1:].strip()
            patient_answer, correct_answer = line.split('|')
            patients_list.append([name, patient_answer, correct_answer])

    return patients_list


# 1.1 бала
def find_mistakes(patient_result: str,
                  correct_result: str) -> tuple[list[int], set[tuple[str, str]]]:
    """
    Знаходить помилки пацієнта. Кожна літера — відповідь на одне питання,
    позиція літери в обох рядках відповідає тому самому питанню.

    Аргументи:
        patient_result: відповіді пацієнта, одна літера на питання
        correct_result: правильні відповіді, такої самої довжини

    Повертає:
        tuple: (positions, pairs)
        - positions: список індексів хибних відповідей за зростанням
        - pairs: множина пар (відповідь пацієнта, правильна відповідь) для
          хибних відповідей; пара, що повторюється на кількох позиціях,
          входить один раз

    Приклад:
        >>> positions, pairs = find_mistakes("ABCD", "ABDF")
        >>> positions
        [2, 3]
        >>> pairs == {("C", "D"), ("D", "F")}
        True
        >>> find_mistakes("ABAB", "CDCD")[1] == {("A", "C"), ("B", "D")}
        True
        >>> find_mistakes("AAAA", "AAAA")
        ([], set())
    """
    positions = []
    pairs = set()

    if patient_result == correct_result:
        return (positions, pairs)

    n = len(correct_result)

    for i in range(n):
        if patient_result[i] != correct_result[i]:
            positions.append(i)
            pairs.add((patient_result[i], correct_result[i]))

    return (positions, pairs)


# 0.6 бала
def mark_mistakes(patient_result: str, positions: list[int]) -> str:
    """
    Будує для лікаря рядок-підказку: '^' під кожною хибною відповіддю
    і '.' під кожною правильною. Рядок має таку саму довжину, як відповіді.

    Аргументи:
        patient_result: відповіді пацієнта
        positions: індекси хибних відповідей (результат find_mistakes)

    Повертає:
        str: рядок-підказка

    Приклад:
        >>> mark_mistakes("ABCD", [2, 3])
        '..^^'
        >>> mark_mistakes("ABCD", [0, 3])
        '^..^'
        >>> mark_mistakes("ABCD", [])
        '....'
    """
    tip = ''
    for i in range(len(patient_result)):
        if i in positions:
            tip += '^'
        else:
            tip += '.'

    return tip


# 1.4 бала
def get_disease(mistake_pairs: set[tuple[str, str]]) -> str:
    """
    Визначає хворобу за множиною пар помилок пацієнта.

    Аргументи:
        mistake_pairs: множина пар помилок (результат find_mistakes)

    Повертає:
        str: ключ із DISEASES_DICT, чий набір характерних помилок має
        найбільше спільних пар із mistake_pairs, або "healthy", якщо жодна
        хвороба не має спільних пар; якщо кілька хвороб мають однакову
        кількість спільних пар, перемагає перша в DISEASES_DICT (вміст
        DISEASES_DICT може змінитися, не покладайтеся на нього)

    Приклад:
        >>> get_disease({("A", "B")})
        'astigmatism'
        >>> get_disease({("A", "B"), ("F", "D")})
        'cataracts'
        >>> get_disease({("C", "D")})
        'healthy'
    """

    max_matches = 0

    result_disease = "healthy"

    for disease, mistakes in DISEASES_DICT.items():
        matches = 0

        for pair in mistake_pairs:
            if pair in mistakes:
                matches += 1

        if matches > max_matches:
            max_matches = matches
            result_disease = disease

    return result_disease


# 1.2 бала
def format_report(patients: list[list[str]]) -> list[list[str]]:
    """
    Діагностує всіх пацієнтів і складає звіт.

    Для кожного пацієнта у звіті є список
        [прізвище ім'я, відповіді, рядок-підказка, хвороба]
    де рядок-підказка — з mark_mistakes, а хвороба — з get_disease.
    Пацієнти йдуть в алфавітному порядку
    (за прізвищем, а за однакового прізвища — за ім'ям). Переданий список
    має лишитися без змін.

    Аргументи:
        patients: список у форматі результату read_file

    Повертає:
        list[list[str]]: список рядків для кожного пацієнта

    Приклад:
        >>> format_report([['Franko Ivan', 'ABCD', 'ABDF']])
        [['Franko Ivan', 'ABCD', '..^^', 'healthy']]
        >>> patients = [['Kosach Olena', 'AAAA', 'AAAA'], ['Franko Ivan', 'XYZA', 'XYZB']]
        >>> format_report(patients)[0]
        ['Franko Ivan', 'XYZA', '...^', 'astigmatism']
        >>> format_report(patients)[1]
        ['Kosach Olena', 'AAAA', '....', 'healthy']
        >>> patients[0][0]
        'Kosach Olena'
    """
    report = []

    for patient in patients:
        name, patient_answer, correct_answer = patient
        positions, patient_result = find_mistakes(patient_answer, correct_answer)
        tip = mark_mistakes(patient_answer, positions)
        disease = get_disease(patient_result)
        report.append([name, patient_answer, tip, disease])

    report = sorted(report)
    return report


# 1.3 бала
def write_report(report: list[list[str]], filepath: str) -> None:
    """
    Записує звіт у файл у порядку звіту: прізвище та ім'я пацієнта в першому
    рядку, далі кожне інше значення в окремому рядку з відступом у 4 пробіли;
    пацієнти відокремлені одним порожнім рядком.

    Аргументи:
        report: список списків пацієнтів у форматі результату format_report
        filepath: шлях до файлу, куди записати звіт

    Приклад:
        >>> import tempfile, os
        >>> with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as out:
        ...     pass
        >>> write_report([['Franko Ivan', 'ABCD', '^...', 'astigmatism'],
        ...               ['Kosach Olena', 'AA', '..', 'healthy']], out.name)
        >>> with open(out.name, encoding='utf-8') as file:
        ...     print(file.read(), end='')
        Franko Ivan
            ABCD
            ^...
            astigmatism
        <BLANKLINE>
        Kosach Olena
            AA
            ..
            healthy
        >>> os.remove(out.name)
    """

    with open(filepath, 'w', encoding='utf-8') as file:
        n = len(report)
        counter  = 0
        for name, result, wrong, diagnosis in report:
            file.write(f'{name}\n')
            counter +=1
            if counter == n:
                file.write(f'    {result}\n    {wrong}\n    {diagnosis}')
            else:
                file.write(f'    {result}\n    {wrong}\n    {diagnosis}\n\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
