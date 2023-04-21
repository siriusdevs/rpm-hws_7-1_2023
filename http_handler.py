import socket
from http.server import BaseHTTPRequestHandler

import requests

from db_utils import DbHandler
from config import *
from json import loads
from views import ips, main_page, error_page, ips_tools, sendMail
from dotenv import load_dotenv
from os import getenv

load_dotenv()

YANDEX_KEY = getenv('YANDEX_KEY')


class InvalidQuery(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname} error: {self.message}'


class CustomHandler(BaseHTTPRequestHandler):
    def page(self, query: dict):
        if self.path.startswith(IPS):
            return ips(DbHandler.get_data(query))
        elif self.path.startswith(IPS_TOOLS):
            return ips_tools()

    def get_template(self) -> tuple:
        if self.path.startswith((IPS, IPS_TOOLS)):
            try:
                query = self.parse_query()
                if query and query.get('mail') is not None:
                    sendMail(query['mail'])
                    return OK, self.page(query)
            except Exception as error:
                return BAD_REQUEST, error_page(str(error))
            return OK, self.page(query)
        return OK, main_page()

    def parse_query(self) -> dict:
        if self.path.startswith(IPS):
            possible_attrs = IPS_ALL_ATTRS
        elif self.path.startswith(IPS_TOOLS):
            possible_attrs = IPS_TOOLS_MAIL_ATR
        else:
            possible_attrs = None
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query_data]
            query = {key: int(value) if value.isdigit() else value for key, value in attrs_values}
            if possible_attrs:
                attrs = list(filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    self.respond(BAD_REQUEST, "Request error")
                    return None
            return query
        return None

    def get(self):
        self.respond(*self.get_template())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            return loads(self.rfile.read(content_length).decode())
        return {}

    def delete(self):
        if self.path.startswith(IPS):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'DELETE FAILED'
            if DbHandler.delete(query):
                return OK, f'Content has been deleted {self.path}'
        else:
            return BAD_REQUEST, "Invalid path"
        return NOT_FOUND, 'Content not found'

    # добавление

    def post(self, content: dict = None):
        if self.path.startswith(IPS):
            content = content if content else self.read_content_json()
            print(content)
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            for attr in content.keys():
                if attr not in IPS_ALL_ATTRS:
                    return NOT_IMPLEMENTED, f'ips do not have attribute: {attr}'
            if all([key in content for key in IPS_REQUIRED_ATTRS]):
                content['local_ip'] = socket.gethostbyname(socket.gethostname())
                content['public_ip'] = requests.get("http://api.ipify.org").text
                status, message = DbHandler.insert(content)
                message = f'http://{HOST}:{PORT}{IPS}/?id={message}' if status == CREATED else message
                return status, message
            return BAD_REQUEST, f'Required keys to add: {IPS_REQUIRED_ATTRS}'
        return BAD_REQUEST, "Invalid path"

    # Изменение

    def put(self):
        if self.path.startswith(IPS):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, 'No content or incorrect data provided by PUT'
            query = self.parse_query()
            if query:
                attrs = list(filter(lambda attr: attr not in IPS_ALL_ATTRS, query.keys()))
                if attrs:
                    return NOT_IMPLEMENTED, f'ips do not have attributes: {attrs}'
            res = DbHandler.update(where=query, data=content)
            if not res:
                return self.post(content)
            return_path = self.path.split('?')[0]
            return OK, f"http://{HOST}:{PORT}{return_path}?id={res[0]}: {self.command} OK"

    def check_auth(self):
        auth = self.headers.get(AUTH, '').split()
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        methods = {
            'PUT': self.put,
            'POST': self.post,
            'DELETE': self.delete
        }
        if self.command == 'GET':
            self.get()
            return
        if self.command in methods.keys():
            process = methods[self.command]
        else:
            self.respond(NOT_IMPLEMENTED, 'Unknown request method')
            return
        if self.check_auth():
            self.respond(*process())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_PUT(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()

    def do_POST(self):
        self.process_request()

    def do_GET(self):
        self.process_request()
