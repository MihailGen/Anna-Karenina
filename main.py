import datetime
import json
from collections import Counter  # Импортируем Counter для подсчета частоты слов
from pathlib import Path
import nltk  # Импортируем Natural Language Toolkit для работы с естественным языком
import requests
from nltk.corpus import stopwords  # Импортируем стоп-слова из NLTK


url = "https://66095c000f324a9a28832d7e.mockapi.io/state"
r = requests.get(url)
path = Path('top_words_list')

top_words_list = {
    "createdAt": datetime.datetime.now().isoformat(),
    "name": "Анна Каренина",
    "avatar": "https://avatar.fandom.com/wiki/Fire_Nation_Man?file=Fire_Nation_Man.png",
    "id": str(int(r.json()[len(r.json()) - 1]['id']) + 1),
}


# Функция для загрузки текста из файла
def load_text(filename):
    try:
        with open(filename, 'rb') as file:  # Открываем файл в режиме чтения в бинарном режиме
            return file.read().decode(
                'utf-8')  # Читаем содержимое файла в байтовом формате и декодируем его в строку с использованием UTF-8
    except FileNotFoundError:
        print("Файл не найден.")
        return None


# Очистка текста от цифр, знаков препинания и стоп-слов
def process_text(text):
    nltk.download('stopwords')
    # Расширяем список стоп-слов
    custom_stopwords = stopwords.words('russian') + ['это', 'этa', 'этот', 'эти', 'которые', 'сказал', 'сказала',
                                                     'который', 'которое',
                                                     'пред', 'говорил', 'говорила', 'очень', 'мог']

    words = text.split()  # Разбиваем текст на слова
    cleaned_words = [word.lower() for word in words if
                     word.isalpha() and word.lower() not in custom_stopwords]  # Оставляем только слова, убираем пунктуацию и цифры, и переводим все слова в нижний регистр. Исключаем стоп-слова
    return cleaned_words  # Возвращаем список очищенных слов


# Подсчет частоты встречаемости слов
def count_words(cleaned_words):
    word_counts = Counter(cleaned_words)  # Создаем словарь с частотой встречаемости слов
    return word_counts


# Отображение наиболее часто встречающихся слов
def display_top_words(word_counts, n=12):
    top_words = word_counts.most_common(n)  # Получаем список самых часто встречающихся слов
    print("Самые часто встречающиеся слова в романе:")
    for word, count in top_words:
        top_words_list[word] = count  # Записываем слова в словарь для дальнейшего "post" на сервер
        print(f"{word}: {count}")  # Выводим слова и их частоту встречаемости

    return top_words


def write_json(path, data):
    try:
        return path.write_text(json.dumps(data), encoding='utf-8')
    except json.decoder.JSONDecodeError:
        print("Invalid JSON")


def main():
    # Загрузка текста романа
    filename = "content/Роман «Анна Каренина».txt"  # Укажите путь к файлу с романом
    text = load_text(filename)
    if text:
        # Очистка текста
        cleaned_words = process_text(text)
        # Подсчет частоты слов
        word_counts = count_words(cleaned_words)
        # Отображение результатов
        display_top_words(word_counts)
        write_json(path, top_words_list)


if __name__ == "__main__":
    main()
