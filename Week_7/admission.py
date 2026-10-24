'''
Lab assignment: read an admission rating list from a file
and write it to a file in CSV format.

Add type hints to both functions for all parameters
and return values.
'''


def read_input_file(pathname: str, number: int) -> list[list[str]]:
    '''
    Read the admission rating list from a text file pathname
    and return a list of lists of strings for the first number students.

    The nested list for one student looks like:
    [rank, full name, admission mark ('+' or '—'), total score, school certificate average]
    All elements are strings. The full name (surname with initials) is a single string.

    Precondition: 0 <= number. If number exceeds the number of students
    in the file, all records are returned.

    :param pathname: str, A path to the txt with admission list
    :param number: int, A capacity of admitted students
    :return: list[list[str]], A nested list of lists for admitted students ratings

    >>> import tempfile, os
    >>> content = ('#\\tПІБ\\tС\\tΣ\\tДЕТАЛІЗАЦІЯ\\tКО\\tКВ\\tД\\n'
    ...     '1\\tМацюк М. І.\\tДо наказу\\t197.859\\t Математика (ЗНО) 197.00\\n'
    ...     ' Середній бал документа про освіту 10.80\\nРК: 1.01\\nСК: —\\n—\\t+\\n'
    ...     '2\\tПроць О. В.\\tДо наказу\\t197.152\\t Математика (ЗНО) 189.00\\n'
    ...     ' Середній бал документа про освіту 11.60\\nРК: 1.01\\nСК: —\\n—\\t+')
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
    ...     _ = tmp.write(content)
    >>> read_input_file(tmp.name, 0)
    []
    >>> read_input_file(tmp.name, 1)
    [['1', 'Мацюк М. І.', '+', '197.859', '10.80']]
    >>> read_input_file(tmp.name, 5)
    [['1', 'Мацюк М. І.', '+', '197.859', '10.80'], ['2', 'Проць О. В.', '+', '197.152', '11.60']]
    >>> os.remove(tmp.name)
    '''

    if number <= 0:
        return []

    with open(pathname, 'r', encoding='utf-8') as file:
        data = file.read()

    lines = data.splitlines()
    if lines[0].startswith('#'):
        lines = lines[1:]

    students =  []
    current_student = None

    for line in lines:
        parts = line.split('\t')
        if parts[0].isdigit():
            # More safe and because pylint complains
            if current_student:
                students.append(current_student)

            if len(students) == number:
                break

            rank, full_name, _, score, _ = parts

            current_student = [rank, full_name, '', score, '']

        elif parts[0].strip().startswith('Середній'):
            if current_student:
                school_average = parts[0].replace('Середній бал документа про освіту', '').strip()
                current_student[4] = school_average

        elif len(parts) > 1 and '—' in parts[0]:
            if current_student:
                current_student[2] = parts[1].strip()

    if current_student and len(students) < number:
        students.append(current_student)

    return students

def write_csv_file(pathname:str, csv_pathname:str) -> None:
    '''
    Write the WHOLE content of the input file pathname to the file
    csv_pathname in CSV format
    (https://en.wikipedia.org/wiki/Comma-separated_values).
    The first line is a header. The function returns nothing.

    This function must use read_input_file.
    Using the csv module of the standard library is forbidden.

    :param pathname: str, A path to the txt with admission list
    :param csv_pathname: str, A path where to write csv file
    :return: None, because only result of function is csv file 

    >>> import tempfile, os
    >>> content = '1\\tМацюк М. І.\\tДо наказу\\t197.859\\t Математика (ЗНО) 197.00\\n\
Середній бал документа про освіту 10.80\\nРК: 1.01\\nСК: —\\n—\\t+'
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
    ...     _ = tmp.write(content)
    >>> with tempfile.NamedTemporaryFile(mode='w', delete=False) as out:
    ...     pass
    >>> write_csv_file(tmp.name, out.name)
    >>> with open(out.name, encoding='utf-8') as csvfile:
    ...     print(csvfile.read().rstrip())
    №,ПІБ,Д,Заг.бал,С.б.док.осв.
    1,Мацюк М. І.,+,197.859,10.80
    >>> os.remove(tmp.name)
    >>> os.remove(out.name)
    '''
    content = read_input_file(pathname, 1000)

    header = '№,ПІБ,Д,Заг.бал,С.б.док.осв.'
    lines = [header]

    for student in content:
        lines.append(','.join(student))

    with open(csv_pathname, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
