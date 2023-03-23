"""Filling html files functions."""
from config import CHARACTERS_TEMPLATE, BOOKS_TEMPLATE, MOVIES_TEMPLATE, MAIN_PAGE, ERROR_PAGE


def list_to_view(iterable: list):
    """Converts data to string with html tags.

    Args:
        iterable : list - data to convert
    """
    return ''.join([f'<ul>{element}</ul>' for element in iterable]) if iterable else '<p>No data given.</p>'


def characters(characters_data: dict) -> str:
    """Fills characters template with character data.

    Args:
        characters_data : dict - data to add
    """
    with open(CHARACTERS_TEMPLATE, 'r') as template:
        return template.read().format(**characters_data)


def books(books_data: dict) -> str:
    """Fills books template with character data.

    Args:
        books_data : dict - data to add
    """
    with open(BOOKS_TEMPLATE, 'r') as template:
        return template.read().format(**books_data)


def movies(movies_data: dict) -> str:
    """Fills movies template with character data.

    Args:
        movies_data : dict - data to add
    """
    with open(MOVIES_TEMPLATE, 'r') as template:
        return template.read().format(**movies_data)


def main_page() -> str:
    """Loads main page template."""
    with open(MAIN_PAGE, 'r') as template:
        return template.read()


def error_page(error: str) -> str:
    """Fills error template with occured error.

    Args:
        error : str - error message
    """
    with open(ERROR_PAGE, 'r') as template:
        return template.read().format(error=error)
