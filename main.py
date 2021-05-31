import csv
import json
import os

from bs4 import BeautifulSoup
import requests


URL = 'http://health-diet.ru/table_calorie/'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0'}


def save_main_html(url: str, headers: dict):
    """
    Функция создает копию страницы с которой необходимо работать.
    :param url: str целевой адрес
    :param headers: dict фейковый юзер-агент
    """
    r = requests.get(url, headers)
    src = r.text

    if not os.path.exists('static'):
        os.mkdir('static')

    with open ('static/main_page.html', 'w') as file:
        file.write(src)


def save_data_json(html_file):
    """
    Функция записывающая названия и ссылки на страницы с которые необходимо обойти в json.
    :param html_file: .html
    """
    with open(html_file) as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    all_products_href = soup.find_all(class_='mzr-tc-group-item-href')

    all_products_dict = {}

    for item in all_products_href:
        item_title = item.text
        item_href = 'http://health-diet.ru' + item.get('href')
        all_products_dict[item_title] = item_href

    with open('static/data.json', 'w') as file:
        json.dump(all_products_dict, file, indent=4, ensure_ascii=False)


with open('static/data.json') as file:
    all_categories = json.load(file)

count = 0
for category_title, category_href in all_categories.items():
    rep = [",", " ", "-", "'"]
    for item in rep:
        if item in category_title:
            category_title = category_title.replace(item, "_")

    r = requests.get(category_href, HEADERS)
    src = r.text

    with open(f'static/{count}_{category_title}.html', 'w') as file:
        file.write(src) # сохраняем все страницы

    with open(f'static/{count}_{category_title}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')

    # Создаем заголовки страницы
    table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
    product = table_head[0].text
    calories = table_head[1].text
    proteins = table_head[2].text
    fats = table_head[3].text
    carbohydrates = table_head[4].text

    with open(f'static/{count}_{category_title}.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(
            (product,
             calories,
             proteins,
             fats,
             carbohydrates)
        )

    products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    for item in products_data:
        product_tds = item.find_all('td')
        product = product_tds[0].find('a').text
        calories = product_tds[1].text
        proteins = product_tds[2].text
        fats = product_tds[3].text
        carbohydrates = product_tds[4].text

        with open(f'static/{count}_{category_title}.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow(
                (product,
                 calories,
                 proteins,
                 fats,
                 carbohydrates)
            )

# TODO добавить в исключения пустые страницы
# TODO добавить вывод процесса на экран
# TODO добавить небольшую задержку в выполнение итераций
# TODO записать данные в json