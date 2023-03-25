"""Various variables."""
# server host and port
HOST = '127.0.0.1'
PORT = 8002

# pages
CHARACTERS = '/character'
BOOKS = '/book'
MOVIES = '/movie'
PAGES = (BOOKS, CHARACTERS, MOVIES)

# templates
TEMPLATES = 'templates/'
MAIN_PAGE = f'{TEMPLATES}index.html'
CHARACTERS_TEMPLATE = f'{TEMPLATES}characters.html'
BOOKS_TEMPLATE = f'{TEMPLATES}books.html'
MOVIES_TEMPLATE = f'{TEMPLATES}movies.html'
ERROR_PAGE = f'{TEMPLATES}error.html'

# HTTP headers
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type', 'text/html'
AUTH = 'Authorization'

# HTTP server error codes
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

# HTTP OK codes
OK = 200
CREATED = 201
NO_CONTENT = 204

# other HTTP codes
NOT_IMPLEMENTED = 501

# db requests
SELECTOR = 'SELECT * FROM {table}'
GET_TOKEN = "SELECT token FROM token WHERE username='{username}'"
INSERT = 'INSERT INTO {table} ({keys}) VALUES ({values})'
UPDATE = 'UPDATE {table} SET {request}'
DELETE = 'DELETE FROM {table} '
SELECT_ID = 'SELECT id from {table}'

# tables parameters
BOOKS_REQUIRED_ATTRS = ['title', 'volume', 'published']
BOOKS_ALL_ATTRS = ['id', 'title', 'volume', 'published']
MOVIES_REQUIRED_ATTRS = ['title', 'duration', 'released']
MOVIES_ALL_ATTRS = ['id', 'title', 'duration', 'released']
CHARACTERS_ALL_ATTRS = ['name']

# table`s names
BOOK = 'book'
MOVIE = 'movie'

# page str to byte coding
CODING = 'utf-8'

# characters const
CHARACTER_META = {'name': None}

API_URL = 'https://the-one-api.dev/v2/character'


# debug messsages
CHARACTER_MSG = 'The Lord of the Rings API'
