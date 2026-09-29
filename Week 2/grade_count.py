prog_basics =  int(input())
math_analysis = int(input())
discrete_math = int(input())
creative_solving = int(input())
history = int(input())

if 0 <= prog_basics <= 100 and 0 <= math_analysis <= 100 and 0 <= discrete_math <= 100 and 0 <= creative_solving <= 100 and 0 <= history <= 100:
    percent_grade = (prog_basics + math_analysis + discrete_math + creative_solving + history) / 5

    if percent_grade >= 90:
        letter_grade = 'A'
    elif percent_grade >= 80:
        letter_grade = 'B'
    elif percent_grade >= 75:
        letter_grade = 'C'
    elif percent_grade >= 65:
        letter_grade = 'D'
    elif percent_grade >= 60:
        letter_grade = 'E'
    else:
        letter_grade = 'F'
        
    print(f'Average grade = {percent_grade:.1f} -> {letter_grade}')
else: 
    print('None')
