from config import CODING, HUMORESKA, MAIN_PAGE, LOGIN


def list_to_view(iterable: list):
    return ''.join(['<ul>{0}</ul>'.format(item) for item in iterable]) if iterable else '<p>No data given.</p>'


def humoreska(humoreska_data: dict) -> bytes:
    with open(HUMORESKA, 'r') as template:
        return template.read().format(**humoreska_data).encode(CODING)


def main_page():
    with open(MAIN_PAGE, 'r') as template:
        return template.read().encode(CODING)


def login_page():
    with open(LOGIN, 'r') as template:
        return template.read().encode(CODING)
