"""Handle http server."""
from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
import json
import config
from views import books, characters, main_page, error_page, movies
from characters import get_character
from dotenv import load_dotenv
from os import getenv


load_dotenv()

API_KEY = getenv('API_KEY')


class InvalidQuery(Exception):
    """Exception raised due to unknown query attributes."""

    def __init__(self, msg: str):
        """Initialize query exception.

        Args:
            msg : str - exception message
        """
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        """Return string representation of an exception."""
        classname = self.__class__.__name__
        return f'{classname} error: {self.message}'


class CustomHandler(BaseHTTPRequestHandler):
    """HTTP Handler."""

    def page(self, query: dict):
        """Define wich index to open.

        Args:
            query : dict - data for the index
        """
        if self.path.startswith(config.BOOKS):
            return books(DbHandler.get_data(config.BOOK, query))
        elif self.path.startswith(config.CHARACTERS):
            return characters(get_character(query))
        elif self.path.startswith(config.MOVIES):
            return movies(DbHandler.get_data(config.MOVIE, query))

    def get_template(self) -> tuple:
        """Get filled template for the pages."""
        if self.path.startswith(config.PAGES):
            try:
                query = self.parse_query()
            except Exception as error:
                return config.BAD_REQUEST, error_page(str(error))
            return config.OK, self.page(query)
        return config.OK, main_page()

    def parse_query(self) -> dict:
        """Validate query parameters.

        Raises:
            InvalidQuery: if query has invalid attributes
        """
        if self.path.startswith(config.BOOKS):
            possible_attrs = config.BOOKS_ALL_ATTRS
        elif self.path.startswith(config.CHARACTERS):
            possible_attrs = config.CHARACTERS_ALL_ATTRS
        elif self.path.startswith(config.MOVIES):
            possible_attrs = config.MOVIES_ALL_ATTRS
        else:
            possible_attrs = None
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query_data]
            query = {key: int(elem) if elem.isdigit() else elem.replace('+', ' ') for key, elem in attrs_values}
            if possible_attrs:
                attrs = list(filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    raise InvalidQuery(f'{__name__} unknown attributes: {attrs}')
            return query
        return None

    def get(self):
        """Send page to server."""
        self.respond(*self.get_template())

    def respond(self, http_code: int, msg: str):
        """Send response, headers and encode template.

        Args:
            http_code : int - response http code
            msg : str - page
        """
        self.send_response(http_code)
        self.send_header(*config.CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(config.CODING))

    def read_content_json(self) -> dict:
        """Read json content."""
        content_length = int(self.headers.get(config.CONTENT_LENGTH, 0))
        if content_length:
            return json.loads(self.rfile.read(content_length).decode())
        return {}

    def delete(self):
        """Proccess DELETE request."""
        if self.path.startswith((config.BOOKS, config.MOVIES)):
            try:
                query = self.parse_query()
            except Exception as error:
                return config.BAD_REQUEST, error_page(str(error))
            if not query:
                return config.BAD_REQUEST, 'DELETE FAILED'
            table = config.BOOK if self.path.startswith(config.BOOKS) else config.MOVIE
            if DbHandler.delete(table, query):
                return config.OK, f'{self.command} OK: http://{config.HOST}:{config.PORT}{self.path}'
        return config.NOT_FOUND, 'Content not found'

    def post(self, material=None):
        """Proccess PUT request.

        Args:
            material : dict - data to put
        """
        if self.path.startswith((config.BOOKS, config.MOVIES)):
            material = self.read_content_json() if material is None else material
            if not material:
                return config.BAD_REQUEST, f'No content provided by {self.command}'
            if self.path.startswith(config.BOOKS):
                all_attr, req_attr, table = config.BOOKS_ALL_ATTRS, config.BOOKS_REQUIRED_ATTRS, config.BOOK
            else:
                all_attr, req_attr, table = config.MOVIES_ALL_ATTRS, config.MOVIES_REQUIRED_ATTRS, config.MOVIE
            for attr in material.keys():
                if attr not in all_attr:
                    return config.NOT_IMPLEMENTED, f'{table} do not have attribute: {attr}'
            if all([key in material for key in req_attr]):
                if DbHandler.insert(table, material):
                    answer = 'OK'
                    put_id = DbHandler.get_id(table, material)
                    return config.CREATED, f'{self.command} {answer}: http://{config.HOST}:{config.PORT}{self.path}?id={put_id}'
                answer = 'FAIL'
                return config.CONFLICT, f'{self.command} {answer}: resource already exists'
            return config.BAD_REQUEST, f'Required keys to add: {req_attr}'
        return config.NO_CONTENT, 'Content not found'

    def put(self):
        """Proccess POST request."""
        if self.path.startswith((config.BOOKS, config.MOVIES)):
            material = self.read_content_json()
            if not material:
                return config.BAD_REQUEST, f'No content provided by {self.command}'
            query = self.parse_query()
            if self.path.startswith((config.BOOKS)):
                all_attr, table = config.BOOKS_ALL_ATTRS, config.BOOK
            else:
                all_attr, table = config.MOVIES_ALL_ATTRS, config.MOVIE
            if query:
                attrs = list(filter(lambda attr: attr not in all_attr, query.keys()))
                if attrs:
                    return config.NOT_IMPLEMENTED, f'{table} do not have attributes: {attrs}'
            res = DbHandler.update(table=table, where=query, data_to=material)
            if not res:
                return self.put(material)
            return config.OK, f'{self.command} OK'

    def check_auth(self):
        """Check authorization for executing requests."""
        auth = self.headers.get(config.AUTH, '').split(' ')
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def process_request(self):
        """Select request method according to command."""
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
            self.respond(config.NOT_IMPLEMENTED, 'Unknown request method')
            return
        if self.check_auth():
            self.respond(*process())
            return
        self.respond(config.FORBIDDEN, 'Auth Fail')

    def do_PUT(self):
        """PUT data."""
        self.process_request()

    def do_DELETE(self):
        """DELETE data."""
        self.process_request()

    def do_POST(self):
        """POST data."""
        self.process_request()

    def do_GET(self):
        """GET data."""
        self.process_request()
