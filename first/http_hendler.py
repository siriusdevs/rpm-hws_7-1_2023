"""File with HTTP handler."""
from config import CONTENT_LENGTH, AUTH, PERSON_PATH, COMPANY_PATH, \
    BAD_REQUEST, OK, MAIN_ATTRS, CONTENT_TYPE, CODING, NOT_FOUND, \
    NOT_IMPLEMENTED, MAIN_REQUIRED_ATTRS, FORBIDDEN, CREATED, \
    NO_CONTENT, PERSON_URL, COMPANY_URL, CLEAR_TABLE_PATH, MAIN_PAGE
from view import get_api_data, people, error_page, main_page, clear_table
from fill_templates import person_template, company_template
from config import HOST, PORT
from http.server import BaseHTTPRequestHandler
from db_utils import DbHandler
from typing import Callable
import json


class CustomHTTP(BaseHTTPRequestHandler):
    """Class which controls http server."""

    def read_content_json(self) -> dict:
        """Method reads and loads headers to json.

        Returns:
            dict - if headers length not Null returns dict of headers.
        """
        content_length = int(self.headers.get(CONTENT_LENGTH, 0))
        check_json = json.loads(self.rfile.read(content_length).decode())
        for element in check_json:
            if element not in MAIN_ATTRS:
                return {}
        if content_length:
            return check_json
        return {}

    def check_auth(self) -> bool:
        """Method checks if CRUD method use correct token and username.

        Returns:
            bool - True if token and username in table for auth.
        """
        auth = self.headers.get(AUTH, "").split()
        if len(auth) == 2:
            return DbHandler.is_valid_token(auth[0], auth[1][1:-1])
        return False

    def page(self, query: dict) -> Callable:
        """Method makes choice between templates for render.

        Args:
            query: dict - dict of params.

        Returns:
            Callable - method for rendering page.
        """
        if self.path.startswith(MAIN_PAGE):
            return people(DbHandler.get_data(query))
        if self.path.startswith(PERSON_PATH):
            return person_template(get_api_data(PERSON_URL))
        if self.path.startswith(COMPANY_PATH):
            return company_template(get_api_data(COMPANY_URL))
        if self.path.startswith(CLEAR_TABLE_PATH):
            DbHandler.remove_data()
            return clear_table()
        return main_page()

    def get_template(self) -> tuple:
        """Method tries getting query from path.

        Returns:
            tuple - statuscode and template.
        """
        if self.path.startswith((PERSON_PATH, COMPANY_PATH, "/")):
            try:
                query = self.parse_query()
            except Exception as error:
                return BAD_REQUEST, error_page(str(error))
            return OK, self.page(query)
        return OK, main_page()

    def parse_query(self) -> list:
        """Method get attrs and conds from path.

        Returns:
            query - list of attrs or conds.
        """
        if self.path.startswith("/"):
            possible_attrs = MAIN_ATTRS
        else:
            possible_attrs = None
        qm_ind = self.path.find("?")
        if "?" in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split("&")
            attrs_values = [line.split("=") for line in query_data]
            query = {key: int(key_v) if key_v.isdigit() else key_v for key, key_v in attrs_values
                     }
            if possible_attrs:
                attrs = list(filter(lambda attr: attr not in possible_attrs, query.keys()))
                if attrs:
                    self.respond(BAD_REQUEST, "Request error")
                    return None
            return query
        return None

    def respond(self, http_code: int, msg: str) -> None:
        """Method sends responses.

        Args:
            http_code: int - statuscode.
            msg: str - message for user.
        """
        self.send_response(http_code)
        self.send_header(*CONTENT_TYPE)
        self.end_headers()
        self.wfile.write(msg.encode(CODING))

    def delete(self) -> tuple:
        """Runs delete method.

        Returns:
            tuple - statuscode and message.
        """
        if self.path.startswith(MAIN_PAGE):
            query = self.parse_query()
            if not query:
                return BAD_REQUEST, "DELETE FAILED"
            if DbHandler.delete(query):
                return OK, f"http://{HOST}:{PORT}{self.path}: DELETE OK"
        return NOT_FOUND, "Content not found"

    def put(self, record: dict = None) -> tuple:
        """Runs put method.

        Args:
            record: dict - dict of params.

        Returns:
            tuple - statuscode and message.
        """
        if self.path.startswith(MAIN_PAGE):
            record = record if record else self.read_content_json()
            if not record:
                return BAD_REQUEST, f"No content provided by {self.command}"
            for attr in record.keys():
                if attr not in MAIN_ATTRS:
                    return NOT_IMPLEMENTED, f"people do not have attribute: {attr}"
            if all([key in record for key in MAIN_REQUIRED_ATTRS]):
                answer = "OK" if DbHandler.insert(record) else "FAIL"
                return CREATED, f"http://{HOST}:{PORT}{self.path}: {self.command} {answer}"
            return BAD_REQUEST, f"Required keys to add: {MAIN_REQUIRED_ATTRS}"
        return NO_CONTENT, "Content not found"

    def post(self) -> tuple:
        """Runs post or update method.

        Returns:
            tuple - statuscode and message.
        """
        if self.path.startswith(MAIN_PAGE):
            record = self.read_content_json()
            if not record:
                return BAD_REQUEST, f"No record provided by {self.command}"
            query = self.parse_query()
            if query:
                attrs = list(filter(lambda attr: attr not in MAIN_ATTRS, query.keys()))
                if attrs:
                    return NOT_IMPLEMENTED, f"people do not have attributes: {attrs}"
            res = DbHandler.update(record=record, where=query)
            if not res:
                return self.put(record)
            return OK, f"http://{HOST}:{PORT}{self.path}: {self.command} OK"

    def get(self) -> None:
        """Runs get template method."""
        self.respond(*self.get_template())

    def process_request(self) -> None:
        """Method makes choice between CRUD methods."""
        methods = {
            "PUT": self.put,
            "POST": self.post,
            "DELETE": self.delete
        }
        if self.command == "GET":
            self.get()
            return
        if self.command in methods.keys():
            process = methods[self.command]
        else:
            self.respond(NOT_IMPLEMENTED, "Unknown request method")
            return
        if self.check_auth():
            new_proc = process()
            if new_proc:
                self.respond(*new_proc)
            else:
                self.respond(NOT_FOUND, "Go to /main")
            return
        self.respond(FORBIDDEN, "Auth Fail")

    def do_PUT(self) -> None:
        """Method called when server get "put" request."""
        self.process_request()

    def do_DELETE(self) -> None:
        """Method called when server get "delete" request."""
        self.process_request()

    def do_POST(self) -> None:
        """Method called when server get "post" request."""
        self.process_request()

    def do_GET(self) -> None:
        """Method called when server get "get" request."""
        self.process_request()
