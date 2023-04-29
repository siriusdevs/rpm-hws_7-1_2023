import smtplib
from urllib.parse import unquote
import db_utils
from config import *
from dotenv import load_dotenv
from os import getenv


load_dotenv()
SMTP_MAIL_PASSWORD = getenv('SMTP_MAIL_PASSWORD', default='mplmohhrjunxltxw')
SMTP_MAIL = getenv('SMTP_MAIL', default="gorachiepechki@yandex.ru")
# Оставлю для теста


def list_to_view(iterable: list):
    res = ''
    if iterable:
        for item in iterable:
            res = res + '<tr>'
            for line in item:
                res = res + f'<td>{line}</td>'
            res = res + '</tr>'
    else:
        res = '<tr><td>No data given.</td></tr>'
    return res


def ips(ips_data: dict) -> str:
    with open(IPS_TEMPLATE, 'r') as template:
        page = template.read()
        return page.format(**ips_data)


def ips_tools() -> str:
    with open(IPS_TOOLS_TEMPLATE, 'r') as template:
        return template.read()


def sendMail(mailto) -> None:
    mailto = unquote(mailto)
    subject = "IP"
    db_utils.DbHandler.db_cursor.execute(SELECTOR)
    res_db = db_utils.DbHandler.db_cursor.fetchall()
    email_text = ''.join([f'{item}\n' for item in res_db]) if res_db else 'No data given.'
    message = f"From: {SMTP_MAIL}\nTo: {mailto}\nSubject: {subject}\n\n{email_text}"
    mail_port = 465         # It`s const
    with smtplib.SMTP_SSL("smtp.yandex.ru", mail_port) as server:
        server.login(SMTP_MAIL, SMTP_MAIL_PASSWORD)
        server.sendmail(SMTP_MAIL, mailto, message.format(
            SMTP_MAIL,
            mailto,
            subject,
            email_text).encode("utf-8"))


def main_page() -> str:
    with open(MAIN_PAGE, 'r') as template:
        return template.read()


def error_page(error: str) -> str:
    with open(ERROR_PAGE, 'r') as template:
        return template.read().format(error=error)
