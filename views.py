from config import *


def answer(answer_data: dict) -> str:
    with open(ANSWER_TEMPLATE, 'r') as template:
        return template.read().format(gif=answer_data["image"], answer=answer_data["answer"])


def main_page() -> str:
    with open(MAIN_PAGE, 'r') as template:
        return template.read()


def quote(quote_data):
    with open(QUOTE_TEMPLATE, 'r') as template:
        return template.read().format(quote=quote_data["quote"]["body"], author=quote_data["quote"]["author"])


def frombase_to_main(iterable: list):
    if not iterable:
        return '<p>No data given.</p>'
    return ''.join([f'<li style="font-size: 30px;">{item}</li>' for item in iterable])
