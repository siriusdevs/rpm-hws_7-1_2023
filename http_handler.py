from config import *
from http.server import BaseHTTPRequestHandler
from views import answer, quote, frombase_to_main
from get_request.quote import get_quote
from json import loads
from get_request.Yes_or_No import get_answer
from db_handler import DbHandler


class CastomHandler(BaseHTTPRequestHandler):

    @staticmethod
    def main_page():
        with open(MAIN_PAGE, 'r') as template:
            return template.read().format(phrases=frombase_to_main(DbHandler.get_data()))

    def parse_query(self) -> dict:
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('=')
            if "number" not in query_data or not query_data[1].isdigit():
                return False, "Request has incorrect attr 'number' or does not have it"
            query = {query_data[0]: query_data[1]}
            return query, ''
        return None, 'No query'

    def page(self):
        if self.path.startswith(QUOTE_PATH):
            return quote(get_quote())

        elif self.path.startswith(ANSWER_PATH):
            return answer(get_answer())
        return CastomHandler.main_page()

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        if content_length:
            try:
                data = loads(self.rfile.read(content_length).decode())
            except Exception:
                return {}
            return data
        return {}

    def respond(self, http_code: int, msg: str):
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def delete(self):
        if self.path.startswith(f'{MAIN_PATH}?'):
            query, msg = self.parse_query()
            if not query:
                return BAD_REQUEST, f'DELETE FAILED \n\n{msg}'
            ans, msg = DbHandler.delete(query)
            return (OK, 'Content has been deleted') if ans else (BAD_REQUEST, msg)
        return NOT_FOUND, 'Content not found'

    def post(self, content=None, msg=None):
        note = f'\n\n Database notification: \n {msg}' if msg else ''
        if self.path == MAIN_PATH or self.path.startswith(f'{MAIN_PATH}?'):
            if not content:
                content = self.read_content_json()
            if not content:
                return BAD_REQUEST, f'No content provided by {self.command}{note}'
            attr = list(content.keys())[0]
            if attr not in POSIB_BODY_KEY:
                return NOT_IMPLEMENTED, f'students do not have attribute: {attr}'

            ans_bl, ind = DbHandler.insert(content)
            return (CREATED, f'{self.command} OK {OBJ_PATH.format(ind=ind)}') if ans_bl else (BAD_REQUEST, f'Incorrect values {note}')
        return NOT_FOUND, 'Content not found'

    def put(self):
        if self.path == MAIN_PATH or self.path.startswith(f'{MAIN_PATH}?'):
            content = self.read_content_json()
            if not content:
                return BAD_REQUEST, 'No content or incorrect data provided by PUT'
            query, msg = self.parse_query()
            print(msg)
            if query:
                attr = list(query.keys())[0]
                if attr not in POSIB_ATTRS:
                    return NOT_IMPLEMENTED, f'titles do not have attribute: {attr}'

            ans, msg = DbHandler.update(where=query, data=content)
            return (self.post(content, msg)) if not ans else (OK, 'PUT OK')
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
