import numpy as np
import random
import string

from english_words import get_english_words_set


def get_text_of_random_chars(size):
    """
    Возвращает текст из случайных символов в количестве size
    """
    letters = string.ascii_lowercase + ' '  # Алфавит: ASCII-символы и пробел
    random_chars_text = np.random.choice(list(letters), size, replace=True)
    random_chars_text = ''.join(random_chars_text)
    return random_chars_text


def get_text_of_random_words(size):
    """
    Возвращает текст из количества size английских слов в случайном порядке
    """
    cur_len = 0
    words_for_text = []
    english_words = list(get_english_words_set(['web2'], lower=True))  # 234450 слов, при каждом запуске программы
    # слова разные
    while cur_len <= size:
        random_word = random.choice(english_words)
        cur_len += len(random_word) + 1
        words_for_text.append(random_word)
    result = ' '.join(words_for_text)[:size]
    return result


def get_great_gatsby_text():
    with open('The-Great-Gatsby.txt') as f:
        full_text_with_punctuation = f.read().replace('\n', ' ').replace('\r', '').lower()
        punctuation = set(string.punctuation)
        return ''.join(c for c in full_text_with_punctuation if c not in punctuation)


def compare(text1, text2):
    assert len(text1) == len(text2)  # Проверяем, что у текстов одинаковая длина
    matched = 0
    for c1, c2 in zip(text1, text2):
        if c1 == c2:
            matched += 1
    return matched / len(text1) * 100  # Получаем процент совпадений


if __name__ == "__main__":
    size = 125000  # Длина текста
    gatsby_text = get_great_gatsby_text()  # Длина - 257427 символов
    real_text1 = gatsby_text[:size]  # получаем текст длиной size - первая часть осмысленного текста
    real_text2 = gatsby_text[size:2 * size]  # получаем текст длиной size - следующая часть осмысленного текста
    random_chars1 = get_text_of_random_chars(size)
    random_words1 = get_text_of_random_words(size)
    random_chars2 = get_text_of_random_chars(size)
    random_words2 = get_text_of_random_words(size)

    print("Процент совпадения двух текстов:")
    print(f"Два осмысленных текста на естественном языке: {compare(real_text1, real_text2)} процентов")
    print(f"Осмысленный текст и текст из случайных букв: {compare(real_text1, random_chars1)} процентов")
    print(f"Осмысленный текст и текст из случайных слов: {compare(real_text1, random_words1)} процентов")
    print(f"Два текста из случайных букв: {compare(random_chars1, random_chars2)} процентов")
    print(f"Два текста из случайных слов: {compare(random_words1, random_words2)} процентов")

    """
    Процент совпадения двух текстов:
    Два осмысленных текста на естественном языке: 7.4048 процентов
    Осмысленный текст и текст из случайных букв: 3.6159999999999997 процентов
    Осмысленный текст и текст из случайных слов: 6.304800000000001 процентов
    Два текста из случайных букв: 3.6656 процентов
    Два текста из случайных слов: 6.1208 процентов
    """


