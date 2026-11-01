"""
Analysis of the Google Chrome browser history.

A visit is a tuple (url, title, date, time, duration):
url and title are str, date is "yyyy-mm-dd", time is "hh:mm:ss.ffffff",
duration is an int (microseconds). The list of visits may be
in any order, not necessarily chronological.
"""


def sites_on_date(visits: list, date: str) -> set[str]:
    """
    Returns the set of all urls that have been visited on the given date.

    :param visits: all visits in the browser history
    (you get it as the result of the function get_chrome_os
    from get_browser_history module)
    :param date: date in format "yyyy-mm-dd"
    :return: set of urls visited on date

    >>> visits = [('https://a.com/', 'A', '2024-10-01', '10:00:00.000000', 100),
    ...           ('https://b.com/', 'B', '2024-10-02', '11:00:00.000000', 300),
    ...           ('https://a.com/', 'A', '2024-10-02', '12:00:00.000000', 200)]
    >>> sites_on_date(visits, '2024-10-02') == {'https://a.com/', 'https://b.com/'}
    True
    >>> sites_on_date(visits, '2024-10-03')
    set()
    """

    url_set = set()

    for url, _, date_of_visit, _, _ in visits:
        if date_of_visit == date:
            url_set.add(url)

    return url_set


def most_frequent_sites(visits: list, number: int) -> set[str]:
    """
    Returns the set of 'number' most frequently visited urls.

    If several urls have the same number of visits, the urls that are
    smaller by the built-in string comparison are chosen first.
    If number is greater than the number of different urls, the set of
    all visited urls is returned.

    :param visits: all visits in browser history
    :param number: number of most frequent sites to return
    :return: set of most frequent sites

    >>> visits = [('https://a.com/', 'A', '2024-10-01', '10:00:00.000000', 100),
    ...           ('https://b.com/', 'B', '2024-10-02', '11:00:00.000000', 300),
    ...           ('https://a.com/', 'A', '2024-10-02', '12:00:00.000000', 200)]
    >>> most_frequent_sites(visits, 1)
    {'https://a.com/'}
    >>> most_frequent_sites(visits, 5) == {'https://a.com/', 'https://b.com/'}
    True
    """

    url_list = []
    for visit in visits:
        url = visit[0]
        url_list.append(url)

    url_list_unique = list(set(url_list))

    url_rank = []
    for url in url_list_unique:
        popularity = url_list.count(url)
        # sort() in ascending order, so minus before to sort right
        url_rank.append((-popularity, url))

    url_rank.sort()

    result = set()
    for url in url_rank[:number]:
        result.add(url[1])

    return result


def get_url_info(visits: list, url: str) -> tuple:
    """
    Returns a tuple with info about the site with the given url:
    title - title of the site (from its last visit)
    last_visit_date - date of the last visit of this site, "yyyy-mm-dd"
    last_visit_time - time of the last visit of this site, "hh:mm:ss.ffffff"
    num_of_visits - how many times this site was visited
    average_time - average duration of a visit to this site

    If the url was not visited, title and last visit date/time are
    empty strings, number of visits and average time are zeros.

    :param visits: all visits in browser history
    :param url: url of site to search
    :return: (title, last_visit_date, last_visit_time, num_of_visits, average_time)

    >>> visits = [('https://a.com/', 'A', '2024-10-01', '10:00:00.000000', 100),
    ...           ('https://b.com/', 'B', '2024-10-02', '11:00:00.000000', 300),
    ...           ('https://a.com/', 'A', '2024-10-02', '12:00:00.000000', 200)]
    >>> get_url_info(visits, 'https://a.com/')
    ('A', '2024-10-02', '12:00:00.000000', 2, 150.0)
    >>> get_url_info(visits, 'https://c.com/')
    ('', '', '', 0, 0)
    >>> visits = [('https://a.com/', 'A', '2025-10-01', '10:00:00.000000', 100),
    ...           ('https://b.com/', 'B', '2024-10-02', '11:00:00.000000', 300),
    ...           ('https://a.com/', 'A', '2023-10-02', '12:00:00.000000', 200)]
    >>> get_url_info(visits, 'https://a.com/')
    ('A', '2025-10-01', '10:00:00.000000', 2, 150.0)
    >>> visits = [('https://a.com/', 'A', '2025-10-01', '10:00:00.000000', 100),
    ...           ('https://b.com/', 'B', '2024-10-02', '11:00:00.000000', 300),
    ...           ('https://a.com/', 'A', '2025-10-01', '10:00:00.000001', 200)]
    >>> get_url_info(visits, 'https://a.com/')
    ('A', '2025-10-01', '10:00:00.000001', 2, 150.0)
    """

    num_of_visits = 0
    all_time_spent = 0
    info = ()

    latest_date = ''
    latest_time = ''
    latest_title = ''

    for visit in visits:
        if url == visit[0]:
            _, title, visit_date, visit_time, time_spent = visit
            num_of_visits += 1
            all_time_spent += time_spent

            current_timestamp = visit_date + ' ' + visit_time
            latest_timestamp = latest_date + ' ' + latest_time

            if current_timestamp >= latest_timestamp:
                latest_date = visit_date
                latest_time = visit_time
                latest_title = title

            info = (latest_title, latest_date, latest_time, '', '')

    if not info:
        return ('', '', '', 0, 0)

    info = (latest_title, latest_date, latest_time, num_of_visits, all_time_spent/num_of_visits)

    return info


if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
