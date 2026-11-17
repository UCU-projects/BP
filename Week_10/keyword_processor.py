"""
Working with IMDb keywords: films and their keywords.
"""


def leave_keyword_from_file(file_input: str, keyword: str, file_output: str) -> int:
    """Writes to the output file only the films that have the given keyword.

    All the text before the keywords list (sections 1-7 and the header of
    section 8) is copied unchanged. In the keywords list, all the lines of
    a film are kept if one of them has the given keyword, otherwise all the
    lines of this film are removed.

    Args:
        file_input (str): The input file containing the keywords.
        keyword (str): The keyword the films in the output file must have.
        file_output (str): The output file to write the filtered keywords.

    Returns:
        int: The number of lines of the keywords list removed from the input file.

    Examples:
        >>> leave_keyword_from_file('keywords.list', 'friendship', 'keywords_updated.list')
        3725264
        >>> keywords = create_film_keywords_dictionary('keywords_updated.list')
        >>> sum(len(values) for values in keywords.values())
        233878
        >>> values = iter(keywords.items())
        >>> movie, keywords = next(values)
        >>> movie
        '"#ATown" (2014)'
        >>> keywords == {'friendship', 'texas', 'drugs', 'beer', 'austin-texas', 'love',
        ...              'web-series'}
        True
        >>> movie, keywords = next(values)
        >>> movie
        '"11-11 En mi cuadra nada cuadra" (2013)'
        >>> keywords == {'friendship', 'pop-star', 'movie-director', 'inventor', 'time-machine',
        ...              'geek', 'cooking', 'musician', 'price-of-fame', 'singing', 'star',
        ...              'mad-scientist', 'time-travel', 'missing-mother', 'teenage-love'}
        True
        >>> leave_keyword_from_file('keywords.list', 'doctor-who', 'keywords_updated.list')
        3946103

    """
    with (
        open(file_input, 'r', encoding='latin-1') as file,
        open(file_output, 'w', encoding='latin-1') as file_in):
        for line in file:
            file_in.write(line)
            if line.rstrip('\n') == '8: THE KEYWORDS LIST':
                break

        for _ in range(2):
            file_in.write(next(file, ''))

        previous_film = None
        new_lines = []
        keyword_flag = False
        removed_lines = 0

        for line in file:
            parts = line.rstrip('\n').split('\t')
            key = parts[-1]
            film = parts[0]

            if previous_film is not None and previous_film != film:
                if keyword_flag:
                    file_in.writelines(new_lines)
                else:
                    removed_lines += len(new_lines)
                keyword_flag = False
                new_lines = []

            previous_film = film
            new_lines.append(line)
            if keyword == key:
                keyword_flag = True

        if new_lines:
            if keyword_flag:
                file_in.writelines(new_lines)
            else:
                removed_lines += len(new_lines)

        return removed_lines


def create_film_keywords_dictionary(filename: str) -> dict[str, set[str]]:
    """Creates a dictionary where the key is the name of the movie
    and the year in brackets as in the file, and the values
    are the set of keywords.

    Args:
        filename (str): The name of the file containing the keywords.

    Returns:
        dict[str, set[str]]: A dictionary with movie names and years as keys
                             and sets of keywords as values.

    Examples:
        >>> keywords = create_film_keywords_dictionary('keywords.list')
        >>> sum(len(values) for values in keywords.values())
        3959142
        >>> values = iter(keywords.items())
        >>> next(values)
        ('"#1 Single" (2006)', {'number-in-title'})
        >>> next(values)
        ('"#1MinuteNightmare" (2014)', {'web-series'})
        >>> movie = next(values)
        >>> movie[0]
        '"#30Nods" (2016)'
        >>> movie[1] == {'friend', 'vlog', 'heroin'}
        True
        >>> keywords['"Doctor Who" (2005) {42 (#3.7)}'] == {
        ...     '42nd-century', 'digit-in-episode-title', 'doctor-who',
        ...     'man-wearing-a-spacesuit', 'number-in-episode-title',
        ...     'number-in-title', 'real-time', 'tenth-doctor',
        ...     'time-for-title'
        ... }
        True
    """

    with open(filename, 'r', encoding='latin-1') as file:
        for line in file:
            if line.rstrip('\n') == '8: THE KEYWORDS LIST':
                break

        for _ in range(2):
            file.readline()

        previous_film = None
        db = {}
        keywords = set()
        for line in file:
            parts = line.rstrip('\n').split('\t')
            film = parts[0]
            keyword = parts[-1]

            if previous_film is not None and previous_film != film:
                db[previous_film] = keywords
                keywords = set()

            previous_film = film
            keywords.add(keyword)

        if previous_film is not None:
            db[previous_film] = keywords

    return db


def find_films_with_max_keywords(film_keywords: dict[str, set[str]],
                                 num_of_films: int) -> list[tuple]:
    """Finds the films with the maximum number of keywords.

    Args:
        film_keywords (dict): A dictionary where the key is the name of the movie
                              and the year in brackets, and the values are sets of keywords.
        num_of_films (int): The number of films to return.

    Returns:
        list[tuple]: A list of tuples where each tuple contains the name of the film
                     and the number of keywords, sorted by the number of keywords
                     in descending order. If the numbers of keywords are equal,
                     the films are sorted by names with usual string comparison.

    Examples:
        >>> film_keywords = create_film_keywords_dictionary('keywords.list')
        >>> films = find_films_with_max_keywords(film_keywords, 3)
        >>> films[0]
        ('Clouds of Sils Maria (2014)', 642)
        >>> films[1:]
        [('The Dark Knight (2008)', 530), ('The Dark Knight Rises (2012)', 446)]
        >>> films = find_films_with_max_keywords(film_keywords, 100)
        >>> films[99]
        ('The Expendables 2 (2012)', 265)

    """
    film_list = [(film, len(keywords)) for film, keywords in film_keywords.items()]
    film_list.sort(key=lambda item: (-item[-1], item[0]))
    return film_list[:num_of_films]


def find_most_popular_keywords(film_keywords: dict, num_of_keywords: int) -> list[tuple]:
    """Finds the most popular keywords.

    Args:
        film_keywords (dict): A dictionary where the key is the name of the movie
                              and the year in brackets, and the values are sets of keywords.
        num_of_keywords (int): The number of keywords to return.

    Returns:
        list[tuple]: A list of tuples where each tuple contains the keyword
                     and the number of films associated with that keyword, sorted by
                     the number of films in descending order. If the numbers of films
                     are equal, the keywords are sorted with usual string comparison.

    Examples:
        >>> find_most_popular_keywords(create_film_keywords_dictionary('keywords.list'), 3)
        [('character-name-in-title', 40690), \
('independent-film', 30772), ('based-on-novel', 28213)]
        >>> keywords = find_most_popular_keywords(create_film_keywords_dictionary(\
'keywords.list'), 20)
        >>> keywords[19]
        ('violence', 6875)
    """
    popularity = {}
    for keywords in film_keywords.values():
        for keyword in keywords:
            popularity[keyword] = popularity.get(keyword, 0) + 1

    sorted_popularity = sorted(popularity.items(), key=lambda item: (-item[1], item[0]))
    return sorted_popularity[:num_of_keywords]



def find_films_keyword_year(film_keywords: dict, keyword: str, year: int) -> set:
    """Finds films that contain a specific keyword and were released in a specific year.

    A film was released in the year if its name contains the year in brackets,
    for example '(1988)'.

    Args:
        film_keywords (dict): A dictionary where the key is the name of the movie
                              and the year in brackets, and the values are sets of keywords.
        keyword (str): The keyword to search for.
        year (int): The year of release to search for.

    Returns:
        set: A set of film names that match the keyword and year.

    Examples:
        >>> films = create_film_keywords_dictionary('keywords.list')
        >>> find_films_keyword_year(films, 'supernatural', 1988) == {
        ...     'Kumander Bawang (1988)', '"Monsters" (1988) {Rain Dance (#1.19)}',
        ...     'Saturday the 14th Strikes Back (1988)', '"Tian xia" (1988)',
        ...     'A Nightmare on Elm Street 4: The Dream Master (1988)'}
        True
        >>> '"Doctor Who" (2005) {Rose (#1.1)}' in find_films_keyword_year(films, \
'doctor-who', 2005)
        True
    """
    film_set = set()
    for naming, keywords in film_keywords.items():
        if f'({year})' in naming and keyword in keywords:
            film_set.add(naming)

    return film_set

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
