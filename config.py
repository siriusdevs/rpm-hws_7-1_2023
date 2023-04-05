# server host and port
HOST = '127.0.0.1'
PORT = 8001

YES_NO_API_URL = "https://yesno.wtf/api"
ANSWER_RESPONSE_MSG = "YES-NO API"
QOUTE_RESPONSE_MSG = "QOUTE API"


TEMPLATES = 'templates/'
ANSWER_TEMPLATE = f'{TEMPLATES}answer.html'
ERROR_TEMPLATE = f'{TEMPLATES}error.html'
MAIN_PAGE = f'{TEMPLATES}index.html'

ANSWER_PATH = "/answer"
FOOL_GAME_PATH = "/foolgame"
MAIN_PATH = "/main"
PAGES = (ANSWER_PATH, FOOL_GAME_PATH)

QUOTE_API_URL = "https://favqs.com/api/qotd"
QUOTE_PATH = "/quote"
QUOTE_TEMPLATE = f'{TEMPLATES}quote.html'

# HTTP headers
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type', 'text/html'
AUTH = 'Authorization'

# HTTP server error codes
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400
NOT_IMPLEMENTED = 501

# HTTP Ok codes
OK = 200
CREATED = 201

# db requests
GET_TOKEN = "SELECT token FROM token WHERE username='{username}';"
INSERT = 'INSERT INTO {table} ({keys}) VALUES {values};'
UPDATE = "UPDATE {table} SET {colomn}='{new_value}' where {key}={value};"
DELETE = 'DELETE FROM {table} where {key}={value};'
SELECTOR = 'select * from {table} order by number;'
SELECT_NUM = 'select * from {table} WHERE number={number};'

# some db consts
LEN_UUID = -37

# page str to byte coding
CODING = 'KOI8-R'
POSIB_ATTRS = ('number')
POSIB_BODY_KEY = ('phrase')
OBJ_PATH = "\n path to the obj: http://127.0.0.1:8001/main?number={ind}"
