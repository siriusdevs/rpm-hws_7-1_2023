import requests
from jinja2 import Environment, FileSystemLoader

def api_module(sol_date):
    """
    Получает фотографию с API NASA для указанной даты sol_date.
    :param sol_date: Дата для получения фотографии (sol).
    :return: Рендеринг шаблона с фотографией.
    """
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template('template/info.html')
    endpoint = 'https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos'
    api_key = 'YGjdEiolRdZV5T4dDZuq2ifq1ECuPk8PRmKYSueJ'
    query_params = {'api_key': api_key, 'sol': sol_date}
    response = requests.get(endpoint, params=query_params)
    data = response.json()
    try:
        photo = data['photos'][0]['img_src']
        return template.render(photo=photo)
    except IndexError:
        return None
