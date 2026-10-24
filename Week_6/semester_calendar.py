"""
Lab work 6
Creating semester calendar using built-in lib
"""

from calendar import TextCalendar, HTMLCalendar

def get_semester_calendar(output_type: str, year: int, first_month: int, last_month:int) -> str:
    """
    Creating semester calendar using built-in lib calendar
    for some year from first month to last in two types: html or txt

    :param output_type: str, A string which decide how to return('txt' or 'html').
    :param year: int, A integer for year of calendar.
    :param first_month: int, A integer for first month of calendar.
    :param last_month: int, A integer for last month of calendar.
    :return: str, A calendar in either of two types decided by output_type.

    >>> text_cal = get_semester_calendar("txt", 2024, 10, 10)
    >>> "October 2024" in text_cal
    True
    >>> "31" in text_cal
    True
    >>> html_cal = get_semester_calendar("html", 2024, 10, 10)
    >>> "<table" in html_cal and "October 2024" in html_cal
    True
    """

    result = []
    if output_type == "txt":
        cal = TextCalendar()
        for month in range(first_month, last_month + 1):
            result.append(cal.formatmonth(year, month))

    if output_type == "html":
        cal = HTMLCalendar()
        for month in range(first_month, last_month + 1):
            result.append(cal.formatmonth(year, month))

    return "".join(result)


if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
