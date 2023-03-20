"""File with function for rendering pages templates."""
from config import REDIRECT, ERROR_PAGE, CLEAR_TABLE, MAIN
from requests import get


def to_html(key: any, k_val: any) -> str:
    """Function returns data in html.

    Args:
        key: any - key of dict.
        k_val: any - value of dict.

    Returns:
        str - key, value in html tag <ul>.
    """
    return f"<ul>{dict_to_view(k_val)}</ul>" if isinstance(k_val, dict) else f'<ul>{key}: {k_val}</ul>'


def start() -> str:
    """Function reads start page template.

    Returns:
        str - start page template.
    """
    with open(REDIRECT, 'r') as template:
        return template.read()


def dict_to_view(iterable: dict) -> str:
    """Function remakes dict to html readable form.

    Args:
        iterable: dict - dict of values.

    Returns:
        str - joined list of keys and values for html.
    """
    return ''.join(
        [to_html(key, k_val) for key, k_val in iterable.items()]
    ) if iterable else '<p>No data given.</p>'


def list_to_view(iterable: list) -> str:
    """Function remakes dict to html readable form.

    Args:
        iterable: dict - dict of values.

    Returns:
        str - joined list of values for html.
    """
    return ''.join([f'<ul>{new}</ul>' for new in iterable]) if iterable else '<p>No data given.</p>'


def main_page() -> str:
    """Function reads main template.

    Returns:
        str - main page template.
    """
    with open(REDIRECT, "r") as template:
        return template.read()


def error_page(error: str) -> str:
    """Function reads error template.

    Args:
        error: str - error message.

    Returns:
        str - error page template.
    """
    with open(ERROR_PAGE, "r") as template:
        return template.read().format(error=error)


def people(people_data: dict) -> str:
    """Function renders people on page.

    Args:
        people_data: dict - dict of people.

    Returns:
        str - formed page template.
    """
    with open(MAIN, "r") as template:
        page = template.read()
        return page.format(**people_data)


def get_api_data(api_page: str) -> dict:
    """Function gets data from API.

    Args:
        api_page: str - person or company generation path.

    Returns:
        dict - json form data from API.
    """
    return get(f"{api_page}").json().get("data")[0]


def clear_table() -> str:
    """Function renders clear page.

    Returns:
        str - clear_table template.
    """
    with open(CLEAR_TABLE, "r") as template:
        return template.read()


def is_num(num: any):
    """Function checks in value is number.

    Args:
        num: any - value for check.

    Returns:
        bool - if value is number returns True.
    """
    return isinstance(num, (int, float))
