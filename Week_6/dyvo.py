"""
Lab work 6
Inserting word "диво" before every word that starts with flag.
"""

def insert_dyvo(sentence: str, flag: str) -> str:
    """
    Inserting word "диво" before every word that starts with flag.

    :param sentence: str, A sentence that will be transformed
    :param flag: str, A string to highlight before where to insert 'диво'    
    :return: str, A sentence with inserted 'диво' before flag

    >>> insert_dyvo('Кит кота по хвилях катав - кит у воді, кіт на киті', 'ки')
    'Дивокит кота по хвилях катав - дивокит у воді, кіт на дивокиті'
    >>> insert_dyvo('12345678910', 'ки')
    '12345678910'
    >>> insert_dyvo('', 'a')
    ''
    >>> # Final "ки" doesn't contain at the start, so without "диво"
    >>> insert_dyvo('Киткотапохвиляхкатав-китуводі,кітнакиті', 'ки') 
    'Дивокиткотапохвиляхкатав-дивокитуводі,кітнакиті'
    >>> insert_dyvo('Кит Кота По Хвилях Катав - Кит У Воді, Кіт На Киті', 'ки')
    'Дивокит Кота По Хвилях Катав - Дивокит У Воді, Кіт На Дивокиті'
    """

    flag = flag.lower()

    n = len(sentence)
    result = []
    i = 0
    while i < n:
        start = i
        while i < n and not sentence[i].isalpha():
            i += 1
        if i > start:
            result.append(sentence[start:i])

        if i < n:
            word_start = i
            while i < n and sentence[i].isalpha():
                i += 1
            word = sentence[word_start:i]

            if word.lower().startswith(flag):
                prefix = 'Диво' if word[0].isupper() else 'диво'
                result.append(prefix + word.lower())
            else:
                result.append(word)

    return ''.join(result)

if __name__ == '__main__':
    import doctest
    print(doctest.testmod())
