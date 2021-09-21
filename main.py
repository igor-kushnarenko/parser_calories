import csv
import json
import os
import random
import time

from bs4 import BeautifulSoup
import requests

URL = 'http://health-diet.ru/table_calorie/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}


def save_main_html(url: str, headers: dict):
    """
    Функция создает копию стартовой страницы с которой необходимо работать.
    :param url: str целевой адрес
    :param headers: dict фейковый юзер-агент
    """
    r = requests.get(url, headers)
    src = r.text

    if not os.path.exists('static/'):
        os.mkdir('static/')
    with open('static/main_page.html', 'w', encoding='utf-8') as file:
        file.write(src)
    return 'static/main_page.html'


def save_data_json(html_file):
    """
    Функция записывающая названия и ссылки на страницы с которые необходимо обойти в json.
    :param html_file: .html
    """
    with open(html_file, encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

    all_products_dict = {}

    for item in all_products_href:
        item_title = item.text
        item_href = 'http://health-diet.ru' + item.get('href')
        all_products_dict[item_title] = item_href

    with open('static/data.json', 'w', encoding='utf-8') as file:
        json.dump(all_products_dict, file, indent=4, ensure_ascii=False)


def collecting_headers(soup):
    """
    Собирает заголовки для таблицы
    :param soup:
    :return:
    """
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'static/{count}_{category_title}.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (product,
             calories,
             proteins,
             fats,
             carbohydrates)
        )


def collect_data(soup):
    """
    Функция собирает и записывает данные в csv-файл
    :return:
    """
    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    product_info = []

    for item in products_data:
        product_tds = item.find_all('td')
        product = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        product_info.append(
            {
                'Product': product,
                'Calories': calories,
                'Proteins': proteins,
                'Fats': fats,
                "Carbohydrates": carbohydrates
            }
        )

        with open(f'static/{count}_{category_title}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (product,
                 calories,
                 proteins,
                 fats,
                 carbohydrates)
            )
    # Запись конечных данных в json
    with open(f'static/{count}_{category_title}.json', 'a', encoding='utf-8') as file:
        json.dump(product_info, file, indent=4, ensure_ascii=False)


def main():
    global count, category_title

    # Проверка существования сохраненной стартовой страницы
    if not os.path.exists('static/main_page.html'):
        html_file = save_main_html(URL, HEADERS)
        if not os.path.exists('static/data.json'):
            save_data_json(html_file)

    with open('static/data.json', encoding='utf-8') as file:
        all_categories = json.load(file)
    count = 0
    countdown = len(all_categories) - 1
    countdown_str = str(countdown)
    print(f'Всего итераций: {countdown}')
    for category_title, category_href in all_categories.items():
        rep = [",", " ", "-", "'"]
        for item in rep:
            if item in category_title:
                category_title = category_title.replace(item, "_")

        r = requests.get(category_href, HEADERS)
        src = r.text

        with open(f'static/{count}_{category_title}.html', 'w', encoding='utf-8') as file:
            file.write(src)
        with open(f'static/{count}_{category_title}.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')

        alert_block = soup.find(class_='uk-alert-danger')
        if alert_block is not None:
            continue

        collecting_headers(soup)
        collect_data(soup)

        time.sleep(random.randrange(1, 2))
        print(f'Осталось итераций: {countdown}/{countdown_str}')
        countdown -= 1
        if countdown == 0:
            print('Работа завершена!')


if __name__ == '__main__':
    main()
