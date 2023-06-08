"""Класс обо всем, который оказался слишком умным для гита по ошибке WPS232."""
import hmac
import http.cookies
import urllib
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit, parse_qs
from jinja2 import Environment, FileSystemLoader

from api import api_module
from register import (
    check_credentials,
    create_history_table,
    get_user_history,
    register_user,
    save_sol,
    delete_user
)

SECRET_KEY = b'secret_key'


class CustomHandler(BaseHTTPRequestHandler):
    """Класс - обработчик HTTP-запросов.

    Содержит в себе 3 виде запросов - post, get и delete.
    Delete запрос для особо искушенных - в браузере он работать не будет...

    Args:
        BaseHTTPRequestHandler: Обработчик, просто обработчик запросов.

    """

    def is_authenticated(self):
        """Проверка аунтефикации.

        Осуществляет проверку аунтефикации пользователей для /info.

        Returns:
            Возвращает сравнение двух хеш-сигнатур.
        """
        session_id = self.cookies.get('session_id')
        if not session_id:
            return False
        username, signature = session_id.value.split(':')
        expected_signature = hmac.new(SECRET_KEY, msg=username.encode(), digestmod='sha256').hexdigest()
        return hmac.compare_digest(expected_signature, signature)

    def do_get(self):
        """Do_get.

        Возьми и дай - краткий комментарий разработчика.
        """
        self.cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))
        split_path = urlsplit(self.path)
        self.path = split_path.path
        query_params = parse_qs(split_path.query)
        sol_date = query_params.get('sol', [''])[0]

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('template/index.html', 'r') as file:
                self.wfile.write(bytes(file.read(), "utf8"))

        elif self.path == '/info':
            if not self.is_authenticated():  # Проверяем наличие авторизационной сессии
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            self.send_response(200, 'OK')  # используйте HTTP/1.1
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            if sol_date:  # Если дата указана, выполняем запрос к API и отдаём шаблон с фотографией
                rendered_html = api_module(sol_date)  # Передаем дату в api_module
                if rendered_html is None:  # Если нет фотографии, отображаем сообщение об ошибке
                    self.wfile.write(bytes("Oops, error 404, our rover doesn't know how to time travel", "UTF-8"))
            else:  # Если дата не указана, отдаём шаблон без фотографии
                env = Environment(loader=FileSystemLoader('.'), autoescape=True)
                template = env.get_template('template/info.html')
                rendered_html = template.render(photo=None)
            self.wfile.write(bytes(rendered_html, "utf8"))

        elif self.path == '/register':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('template/register.html', 'r') as file:
                self.wfile.write(bytes(file.read(), "utf8"))

        elif self.path == '/history':
            if not self.is_authenticated():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            username, _ = self.cookies.get('session_id').value.split(':')
            user_history = get_user_history(username)

            env = Environment(loader=FileSystemLoader('.'), autoescape=True)
            template = env.get_template('template/history.html')
            rendered_html = template.render(sol_history=user_history)
            self.wfile.write(bytes(rendered_html, "utf8"))

        elif self.path == '/delete_account':
            if not self.is_authenticated():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
            with open('template/delete_account.html', 'r') as file:
                self.wfile.write(bytes(file.read(), "utf8"))

        else:
            self.send_response(404)

    def do_post(self):
        """Do_post.

        Возьми и отправь - краткий комментарий разработчика.
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form = urllib.parse.parse_qs(post_data.decode())
        self.cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

        if self.path == '/login':
            username = form.get('username')[0]
            password = form.get('password')[0]

            if check_credentials(username, password):
                self.send_response(303)
                self.send_header('Location', '/info')
                signature = hmac.new(SECRET_KEY, msg=username.encode(), digestmod='sha256').hexdigest()
                self.send_header('Set-Cookie', f'session_id={username}:{signature}; Path=/; HttpOnly')
                self.end_headers()
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Invalid username or password', 'utf8'))

        elif self.path == '/register':
            username = form.get('username')[0]
            password = form.get('password')[0]
            register_user(username, password)
            create_history_table()

            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()

        elif self.path == '/info':
            sol_date = form.get('sol', [''])[0]  # Извлекаем дату из данных формы
            if sol_date:  # Если дата указана, выполняем запрос к API
                self.send_response(303)
                self.send_header('Location', f'/info?sol={sol_date}')
                self.end_headers()
                username, _ = self.cookies.get('session_id').value.split(':')
                save_sol(username, sol_date)
            else:  # Если дата не указана, возвращаем страницу с сообщением об ошибке или без фото
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Please enter a sol (date)', 'utf8'))

        elif self.path == '/delete_account':
            if not self.is_authenticated():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return

            username, _ = self.cookies.get('session_id').value.split(':')
            delete_user(username)

            self.send_response(303)
            self.send_header('Location', '/')
            self.send_header('Set-Cookie', 'session_id=; expires=Thu, 01 Jan 1970 00:00:00 GMT')
            self.end_headers()
        else:
            self.send_response(404)

    def do_delete(self):
        """Do_delete.

        Возьми и удали - краткий ответ разъярённого разработчика.
        """
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        form = urllib.parse.parse_qs(post_data.decode())
        self.cookies = http.cookies.SimpleCookie(self.headers.get('Cookie'))

        if self.path == '/delete_account':
            if not self.is_authenticated():
                self.send_response(302)
                self.send_header('Location', '/')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes('Not authenticated', 'utf8'))
                return

            username = form.get('username')[0]
            try:
                delete_user(username)
                # After deletion, redirect the user to the homepage
                self.send_response(303)
                self.send_header('Location', '/')
                self.end_headers()
            except Exception as exception:
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(bytes(f'An error occurred: {exception}', 'utf8'))


def run(server_class=HTTPServer, handler_class=CustomHandler):
    """Запуск сервера.

    Да, возьми и запусти.

    Args:
        server_class (_type_, optional): Defaults to HTTPServer.
        handler_class (_type_, optional): Defaults to CustomHandler.
    """
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
