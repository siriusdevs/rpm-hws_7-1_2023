#HTTP
HOST = '127.0.0.1'
PORT = 8002

DEMO_TOKEN = '{b73e83f7-c6c2-4241-8735-1ec2f981b39e}'

#DATABASE LOGIC
INSERT = 'insert into quote (author, body) values (%s, %s)'
DELETE = 'delete from quote where id=%s'
GET = 'select * from quote where id=%s'
GET_ALL_AUTHORS = 'select author from quote'
GET_AUTHOR = 'select id, author, body from quote where author=%s'
UPDATE = 'update quote set author=%s, body=%s where id=%s'
POST_SELECT = 'select body from quote where author=%s'
SELECTOR = 'select * from quote'
DAY_SELECTOR = 'select author, body from quote_day where date=%s'
DATE_SELECTOR = 'select date from quote_day'
DAY_INSERT = "insert into quote_day (date, author, body) values (%s, %s, %s)"
SELECT_TOKEN = 'select token from token where username=%s'
KEYS_AUTHOR = ['id', 'author', 'body', 'token']
SELECT_ID = 'select id from quote where author=%s and body=%s'

#STATUS CODE
FORBIDDEN = {"code": 403, "message": "FORBIDDEN"}
BAD_REQUEST = {"code": 400, "message": "BAD REQUEST"}
NOT_FOUND = {"code": 404, "message": "NOT FOUND"}

#STATUS CODE FOR TESTS
FORBIDDEN_TEST = {'detail' : {"code": 403, "message": "FORBIDDEN"}}
BAD_REQUEST_TEST = {'detail': {"code": 400, "message": "BAD REQUEST"}}
POST_OK = {"code": 201, "message": "CREATED"}
PUT_OK = {"code": 200, "message": "PUT OK"}
DELETE_OK = {"code": 200, "message": "DELETE OK"}
NOT_FOUND_TEST = {'detail': {"code": 404, "message": "NOT FOUND"}}
OK = 200
CREATED = 201
DEFAULT_ADMIN = {"code": "CODE", "message": "MESSAGE"}

#API FOR QUOTE EVERY DAY
URL = 'https://favqs.com/api/qotd'

#HEADERS FOR API REQUEST
HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

####
CURRENT_RESPONSE = {'quotes': [
        {"author": "Maksim Bezborodov",
        'body': 'What does it mean? It means that you are a hole.',
        'id': 2}]}
