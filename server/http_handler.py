from http.server import BaseHTTPRequestHandler
from os import getenv
import psycopg2
from config import OK, FORBIDDEN
from dotenv import load_dotenv
from humoreski import get_humoreska
from views import humoreska, login_page, main_page
from check_user import check_passes
from json import loads as ld

load_dotenv()

API_URL = getenv('API_URL')


class CustomHandler(BaseHTTPRequestHandler):
    def get_template(self) -> bytes:
        if self.headers:
            if "super_auth" not in self.headers["Cookie"]:
                return login_page()
        if self.path.startswith("/humoreska"):
            return humoreska(get_humoreska())
        return main_page()

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
                self.send_header('Set-Cookie', 'super_auth=yes; Max-Age=15')
                self.end_headers()
                self.wfile.write(main_page())
                return
        self.end_headers()
        self.wfile.write(self.get_template())

    def read_content_json(self) -> dict:
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length:
            try:
                data = ld(self.rfile.read(content_length).decode())
            except Exception:
                return {}
            return data
        return {}

    def do_DELETE(self):
        if "Authorization" in self.headers:
            if self.headers["Authorization"] == "q73a3f7-c6c2-4241-8735-1ec2f981b39e":
                query = self.parse_query()
                if query[0] and list(query[0].values())[0]:
                    content = self.read_content_json()
                    db_connection = psycopg2.connect(
                    dbname=getenv("PG_DBNAME"),
                    host=getenv("PG_HOST"),
                    port=getenv("PG_PORT"), user=getenv("PG_USER"),
                    password=getenv("PG_PASSWORD"),
                    )
                    cursor = db_connection.cursor()
                    for key in content.keys():
                        if list(query[0].values())[0] != key:
                            self.respond(400, "Bad request, data in body and in query doesnt match")
                            db_connection.commit()
                            cursor.close()
                            db_connection.close()
                            return
                        cursor.execute("SELECT * FROM users.data where login = '{0}'".format(key))
                        if cursor.fetchall():
                            cursor.execute("DELETE FROM users.data where login = '{0}';".format(key))
                        else:
                            self.respond(400, "Bad request, probably data not exist in db")
                            db_connection.commit()
                            cursor.close()
                            db_connection.close()
                            return
                    self.respond(200, "Succesfully deleted")
                    db_connection.commit()
                    cursor.close()
                    db_connection.close()
                else:
                    if query[1]:
                        self.respond(400, query[1])
                        return
                    else:
                        self.respond(400, "No key in query!")

    def do_PUT(self):
        if "Authorization" in self.headers:
            if self.headers["Authorization"] == "q73a3f7-c6c2-4241-8735-1ec2f981b39e":
                query = self.parse_query()
                if query[0] and list(query[0].values())[0]:
                    content = self.read_content_json()
                    db_connection = psycopg2.connect(
                    dbname=getenv("PG_DBNAME"),
                    host=getenv("PG_HOST"),
                    port=getenv("PG_PORT"), user=getenv("PG_USER"),
                    password=getenv("PG_PASSWORD"),
                    )
                    cursor = db_connection.cursor()
                    for key in content.keys():
                        if list(query[0].values())[0] != key:
                            self.respond(400, "Bad request, data in body and in query doesnt match")
                            db_connection.commit()
                            cursor.close()
                            db_connection.close()
                            return
                        cursor.execute("SELECT * FROM users.data where login = '{0}'".format(key))
                        if cursor.fetchall():
                            self.respond(400, "Bad request, probably data already in db")
                            db_connection.commit()
                            cursor.close()
                            db_connection.close()
                            return
                        else:
                            cursor.execute('INSERT INTO users.data (login, pwd) VALUES {0};'.format((key, content[key])))
                    self.respond(200, "Succesfully inputed ")
                    db_connection.commit()
                    cursor.close()
                    db_connection.close()
                else:
                    if query[1]:
                        self.respond(400, query[1])
                        return
                    else:
                        self.respond(400, "No key in query!")
        else:
            self.respond(403, "Forbidden")

    def handle(self):
        try:
            BaseHTTPRequestHandler.handle(self)
        except BrokenPipeError:
            self.wfile.write(self.get_template())

    def parse_query(self):
        qm_ind = self.path.find('?')
        if '?' in self.path and qm_ind != len(self.path) - 1:
            query_data = self.path[qm_ind + 1:].split('=')
            if query_data[0] != "login":
                return False, "Request has incorrect attr 'login' or does not have it"
            query = {query_data[0]: query_data[1]}
            return query, ''
        return None, 'No query'
