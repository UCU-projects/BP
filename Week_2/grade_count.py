'''Program for calculating grade'''
i = 0
percent_grade = 0
for grade in range(5):
    grade = int(input())
    if 0 <= grade <= 100:
        percent_grade += grade/5
    else:
        i = 1

if i == 0:
    if percent_grade >= 90:
        LETTER_GRADE = 'A'
    elif percent_grade >= 80:
        LETTER_GRADE = 'B'
    elif percent_grade >= 75:
        LETTER_GRADE = 'C'
    elif percent_grade >= 65:
        LETTER_GRADE = 'D'
    elif percent_grade >= 60:
        LETTER_GRADE = 'E'
    else:
        LETTER_GRADE = 'F'
    print(f'Average grade = {percent_grade:.1f} -> {LETTER_GRADE}')
else:
    print('None')
