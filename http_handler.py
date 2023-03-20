from config import *
from http.server import BaseHTTPRequestHandler
from views import answer, quote, frombase_to_main
from get_request.quote import get_quote
from json import loads
from get_request.Yes_or_No import get_answer
from db_handler import DbHandler


class InvalidQuery(Exception):

    def __init__(self, msg: str):
        super().__init__(msg)
        self.message = msg

    def __str__(self):
        classname = self.__class__.__name__
        return f'{classname} error: {self.message}'


class CastomHandler(BaseHTTPRequestHandler):

    @staticmethod
    def main_page():
        with open(MAIN_PAGE, 'r') as template:
            return template.read().format(phrases=frombase_to_main(DbHandler.get_data()))

    def parse_query(self) -> dict:
        possible_attrs = POSIB_ATTRS
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('&')
            attrs_values = [line.split('=') for line in query_data]
            query = {key: int(value) if value.isdigit()
                     else value for key, value in attrs_values}
            if "id" in query and not isinstance(query["id"], int):
                return False
            if possible_attrs:
                attrs = list(
                    filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    raise InvalidQuery(
                        f'{__name__} unknown attributes: {attrs}')
            return query
        return None

    def page(self):
        if self.path.startswith(QUOTE_PATH):
            return quote(get_quote())

        elif self.path.startswith(ANSWER_PATH):
            return answer(get_answer())
        else:
            return CastomHandler.main_page()

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            return loads(self.rfile.read(content_length).decode())

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def delete(self):
        if self.path.startswith(f'{MAIN_PATH}?'):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, 'DELETE FAILED'
            if DbHandler.delete(query):
                return OK, 'Content has been deleted'
        return NOT_FOUND, 'Content not found'

    def post(self, content=None):
        if self.path == MAIN_PATH or self.path.startswith(f'{MAIN_PATH}?'):
            if not content:
                content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            attr = list(content.keys())[0]
            if attr not in POSIB_ATTRS:
                return NOT_IMPLEMENTED, f'students do not have attribute: {attr}'

            answer_bool, ind = DbHandler.insert(content)
            answer = 'OK' if answer_bool else 'FAIL'
            error_code = CREATED if answer == 'OK' else BAD_REQUEST
            return error_code, f'{self.command} {answer} \n path to the obj: http/main?number={ind}'
        return NOT_FOUND, 'Content not found'

    def put(self):
        if self.path == MAIN_PATH or self.path.startswith(f'{MAIN_PATH}?'):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}'
            query = self.parse_query()
            if query:
                attr = list(query.keys())[0]
                if attr not in POSIB_ATTRS:
                    return NOT_IMPLEMENTED, f'titles do not have attribute: {attr}'
            res = DbHandler.update(where=query, data=content)
            if not res:
                return self.post(content)
            return OK, f'PUT OK'
        return NOT_FOUND, 'Content not found'

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
        if self.command in methods.keys():
            process = methods[self.command]
        else:
            self.respond(NOT_IMPLEMENTED, 'Unknown request method')
            return
        if self.check_auth():
            self.respond(*process())
            return
        self.respond(FORBIDDEN, 'Auth Fail')

    def do_GET(self):
        self.respond(OK, self.page())

    def do_PUT(self):
        self.process_request()

    def do_DELETE(self):
        self.process_request()

    def do_POST(self):
        self.process_request()
