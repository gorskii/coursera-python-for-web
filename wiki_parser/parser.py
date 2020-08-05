"""Parser solution for week 2 BeautifulSoup practice task"""

import os
import re
from collections import deque, defaultdict
from typing import List, Dict

from bs4 import BeautifulSoup


def parse(path_to_file: str) -> List[int]:
    """Parse given page and return page statistics"""
    with open(path_to_file, mode='r', encoding='utf-8') as file:
        content = BeautifulSoup(file, 'html.parser').find(id='bodyContent')

    imgs = _count_images_of_min_width_200(content)
    headers = _count_headers_starting_with_e_t_c(content)
    linkslen = _count_max_link_sequence(content)
    lists = _count_unnested_lists(content)

    return [imgs, headers, linkslen, lists]


def build_bridge(path: str, start_page: str, target_page: str) -> List[str]:
    """Возвращает список страниц, по которым можно перейти по ссылкам
    со start_page на target_page, начальная и конечная страницы
    включаются в результирующий список
    """
    local_pages = set(os.listdir(path))

    if start_page == target_page:
        return [start_page]

    visited_pages = set()
    parents = defaultdict(list)
    links = deque([start_page])
    while links:
        current_page = links.popleft()
        if current_page in visited_pages:
            continue
        visited_pages.add(current_page)

        with open(os.path.join(path, current_page), encoding="utf-8") as file:
            inner_links = re.findall(r"(?<=/wiki/)[\w()]+", file.read())
        if not inner_links:
            continue

        if target_page in inner_links:
            parents[target_page].append(current_page)
            break

        for link in inner_links:
            if link in local_pages and link not in visited_pages:
                parents[link].append(current_page)
                links.append(link)

    bridge = _get_shortest_path(start_page, target_page, parents)

    return bridge


def get_statistics(
        path: str, start_page: str, end_page: str
) -> Dict[str, List[int]]:
    """Собирает статистику со страниц, возвращает словарь, где:
    ключ - название страницы,
    значение - список со статистикой страницы"""

    pages = build_bridge(path, start_page, end_page)
    statistic = {
        page: parse(os.path.join(path, page))
        for page in pages
    }
    return statistic


def _count_images_of_min_width_200(content: BeautifulSoup) -> int:
    """Count images of width >= 200"""
    return len(content.find_all('img', width=lambda x: x and int(x) >= 200))


def _count_headers_starting_with_e_t_c(content: BeautifulSoup) -> int:
    """Count headers starting with E, T, or C"""
    headers = 0
    for header in content.find_all(re.compile(r'h[1-6]')):
        if header.text[0] in ('E', 'T', 'C'):
            headers += 1
    return headers


def _count_max_link_sequence(content: BeautifulSoup) -> int:
    """Count maximum link sequence length where there is no other tags
    between links"""
    max_length = 0
    for link in content.find_all('a'):
        current_sequence_length = 0
        current_element = link
        while current_element and current_element.name == 'a':
            current_sequence_length += 1
            current_element = current_element.find_next_sibling()
        if current_sequence_length > max_length:
            max_length = current_sequence_length
    return max_length


def _count_unnested_lists(content: BeautifulSoup) -> int:
    """Count number of unnested <ul> and <ol> lists.
    Using descendants iterator and lambda for a faster search
    """
    lists = 0
    list_tags = ('ul', 'ol')
    for element in content.descendants:
        if element.name in list_tags:
            if not element.find_parent(lambda x: x.name in list_tags):
                lists += 1
    return lists


def _get_shortest_path(
        start_page: str, target_page: str, parents: Dict[str, List[str]]
) -> List[str]:
    """Get shortest path to target_page from it's parents"""
    path = []
    page = target_page
    while parents[page] and page != start_page:
        path.append(page)
        page = parents[page][0]
    path.append(start_page)

    return path[::-1]
