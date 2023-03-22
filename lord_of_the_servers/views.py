from config import *


def list_to_view(iterable: list):
    return ''.join([f'<ul>{item}</ul>' for item in iterable]) if iterable else '<p>No data given.</p>'


def characters(character_data: dict) -> str:
    with open(CHARACTERS_TEMPLATE, 'r') as template:
        return template.read().format(**character_data)


def books(books_data: dict) -> str:
    with open(BOOKS_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**books_data)


def movies(movies_data: dict) -> str:
    with open(MOVIES_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**movies_data)


def main_page() -> str:
    with open(MAIN_PAGE, 'r') as template:
        return template.read()


def error_page(error: str) -> str:
    with open(ERROR_PAGE, 'r') as template:
        return template.read().format(error=error)
