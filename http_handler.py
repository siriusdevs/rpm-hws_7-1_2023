from http.server import BaseHTTPRequestHandler
from os import getenv

from config import *
from dotenv import load_dotenv
from humoreski import get_humoreska
from views import humoreska, login_page, main_page
from check_user import check_passes

load_dotenv()

API_URL = getenv('API_URL')


class CustomHandler(BaseHTTPRequestHandler):
    def get_template(self) -> bytes:
        print("super_auth" in self.headers["Cookie"])
        if "super_auth" not in self.headers["Cookie"]:
            return login_page()
        if self.path.startswith("/humoreska"):
            return humoreska(get_humoreska())
        return main_page()

    def parse_query(self) -> dict:
        if '?' in self.path:
            query = self.path[self.path.find('?') + 1:].split('&')
            attrs_values = [line.split('=') for line in query]
            return {key: int(value) if value.isdigit() else value for key, value in attrs_values}
        return None

    def do_GET(self):
        self.send_response(OK)
        self.send_header('Content-type', 'html')
        self.end_headers()
        self.wfile.write(self.get_template())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header('Content-type', 'text')
        self.end_headers()
        self.wfile.write(msg.encode())

    def process(self):
        if self.check_auth():
            self.respond(*self.make_changes())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_POST(self):
        post_body = str(self.rfile.read(int(self.headers.get('Content-Length'))))
        entered = post_body.replace("login=", "").replace("pass=", "").replace("b", "").replace("'", "").split("&")
        log = entered[0]
        passsword = entered[1]
        logpass_data = check_passes()
        self.send_response(OK)
        if log in logpass_data.keys():
            if logpass_data[log] == passsword:
                self.send_header('Content-type', 'html')
                self.send_header('Set-Cookie', 'super_auth=yes; Max-Age=5')
                self.end_headers()
                self.wfile.write(main_page())
                return
        self.end_headers()
        self.wfile.write(self.get_template())

    def do_DELETE(self):
        self.process()

    def handle(self):
        try:
            BaseHTTPRequestHandler.handle(self)
        except BrokenPipeError:
            self.wfile.write(self.get_template())
