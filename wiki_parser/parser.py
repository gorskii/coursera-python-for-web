import re

from bs4 import BeautifulSoup


def parse(path_to_file):
    imgs = headers = linkslen = lists = 0

    with open(path_to_file, mode='r', encoding='utf-8') as file:
        content = BeautifulSoup(file, 'html.parser').find(id='bodyContent')

    # Count images where width >= 200
    for img in content.find_all('img'):
        width = img.get('width')
        if width:
            if int(width) >= 200:
                imgs += 1

    # Count headers where first letter of inner text is in ('E', 'T', 'C')
    for header in content.find_all(re.compile(r'h[1-6]')):
        if header.text[0] in ('E', 'T', 'C'):
            headers += 1

    return [imgs, headers, linkslen, lists]


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    # напишите вашу реализацию логики по вычисления кратчайшего пути здесь


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""

    # получаем список страниц, с которых необходимо собрать статистику
    pages = build_bridge(path, start_page, end_page)
    # напишите вашу реализацию логики по сбору статистики здесь

    return statistic
