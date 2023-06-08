"""Файл для работы с API, получает sol_date, выдает рендер для шаблона."""

import requests
from jinja2 import Environment, FileSystemLoader

ENDPOINT = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
API = 'YGjdEiolRdZV5T4dDZuq2ifq1ECuPk8PRmKYSueJ'


def api_module(sol_date):
    """Метод для работы с API.

    Метод делает запрос к API, получая дату для обращения,
    возвращает рендер изображения для шаблона.

    Args:
        sol_date (int): дата для вывода рендера.

    Returns:
        photo: рендер для шаблона.

    """
    env = Environment(loader=FileSystemLoader('.'), autoescape=True)
    template = env.get_template('template/info.html')
    query_params = {'api_key': API, 'sol': sol_date}
    response = requests.get(ENDPOINT, params=query_params)
    photo_data = response.json()
    try:
        return template.render(photo=photo_data['photos'][0]['img_src'])
    except IndexError:
        return None
