from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
from config import *
from json import loads
from views import books, characters, main_page, error_page, movies
from characters import get_character
from dotenv import load_dotenv
from os import getenv


load_dotenv()

API_KEY = getenv('API_KEY')


class InvalidQuery(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname} error: {self.message}'


class CustomHandler(BaseHTTPRequestHandler):
    def page(self, query: dict):
        if self.path.startswith(BOOKS):
            return books(DbHandler.get_data(BOOK, query))
        elif self.path.startswith(CHARACTERS):
            return characters(get_character(query))
        elif self.path.startswith(MOVIES):
            return movies(DbHandler.get_data(MOVIE, query))

    def get_template(self) -> tuple:
        if self.path.startswith(PAGES):
            try:
                query = self.parse_query()
            except Exception as error:
                return BAD_REQUEST, error_page(str(error))
            return OK, self.page(query)
        return OK, main_page()

    def parse_query(self) -> dict:
        if self.path.startswith(BOOKS):
            possible_attrs = BOOKS_ALL_ATTRS
        elif self.path.startswith(CHARACTERS):
            possible_attrs = CHARACTERS_ALL_ATTRS
        elif self.path.startswith(MOVIES):
            possible_attrs = MOVIES_ALL_ATTRS
        else:
            possible_attrs = None
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query_data]
            query = {key: int(value) if value.isdigit() else value.replace('+', ' ') for key, value in attrs_values}
            if possible_attrs:
                attrs = list(filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    raise InvalidQuery(f'{__name__} unknown attributes: {attrs}')
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
        """"""
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            return loads(self.rfile.read(content_length).decode())
        return {}

    def delete(self):
        """Proccess DELETE request"""
        if self.path.startswith((BOOKS, MOVIES)):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'DELETE FAILED'
            table = BOOK if self.path.startswith(BOOKS) else MOVIE
            if DbHandler.delete(table, query):
                return OK, 'Content has been deleted'
        return NOT_FOUND, 'Content not found'

    def put(self, content=None):
        """
        Proccess PUT request

        Args:
            content - data to put
        """
        if self.path.startswith((BOOKS, MOVIES)):
            content = self.read_content_json() if not content else content
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            if self.path.startswith(BOOKS):
                all_attr, req_attr, table = BOOKS_ALL_ATTRS, BOOKS_REQUIRED_ATTRS, BOOK
            else:
                all_attr, req_attr, table = MOVIES_ALL_ATTRS, MOVIES_REQUIRED_ATTRS, MOVIE
            for attr in content.keys():
                if attr not in all_attr:
                    return NOT_IMPLEMENTED, f'{table} do not have attribute: {attr}'
            if all([key in content for key in req_attr]):
                answer = 'OK' if DbHandler.insert(table, content) else 'FAIL'
                return CREATED, f'{self.command} {answer}'
            return BAD_REQUEST, f'Required keys to add: {req_attr}'
        return NO_CONTENT, 'Content not found'

    def post(self):
        """Proccess POST request"""
        if self.path.startswith((BOOKS, MOVIES)):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            query = self.parse_query()
            if self.path.startswith((BOOKS)):
                all_attr, table = BOOKS_ALL_ATTRS, BOOK
            else:
                all_attr, table = MOVIES_ALL_ATTRS, MOVIE
            if query:
                attrs = list(filter(lambda attr: attr not in all_attr, query.keys()))
                if attrs:
                    return NOT_IMPLEMENTED, f'{table} do not have attributes: {attrs}'
            res = DbHandler.update(table=table, where=query, data=content)
            print(res)
            if not res:
                return self.put(content)
            return OK, f'{self.command} OK'

    def check_auth(self):
        """
        Check authorization for executing requests
        """
        auth = self.headers.get(AUTH, '').split(' ')
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        """
        Select request method according to command
        """
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
        """PUT data"""
        self.process_request()

    def do_DELETE(self):
        """DELETE data"""
        self.process_request()

    def do_POST(self):
        """POST data"""
        self.process_request()

    def do_GET(self):
        """GET data"""
        self.process_request()
