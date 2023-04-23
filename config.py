# server host and port
HOST = '127.0.0.1'
PORT = 8001

# pages
IPS = '/ips'
IPS_TOOLS = '/tools_ips'
PAGES = (IPS, IPS_TOOLS)

# templates paths
TEMPLATES = 'templates/'
MAIN_PAGE = f'{TEMPLATES}index.html'
IPS_TEMPLATE = f'{TEMPLATES}ips.html'
IPS_TOOLS_TEMPLATE = f'{TEMPLATES}tools_ips.html'
ERROR_PAGE = f'{TEMPLATES}error.html'

# HTTP headers
CONTENT_LENGTH = 'Content-Length'
CONTENT_TYPE = 'Content-Type', 'text/html'
AUTH = 'Authorization'

# HTTP server error codes
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400
INTERNAL_ERROR = 500

# HTTP OK codes
OK = 200
CREATED = 201
NO_CONTENT = 204

# other HTTP codes
NOT_IMPLEMENTED = 501

# db requests
RETURN_ID = "returning id"
SELECTOR = 'SELECT id, name, local_ip, public_ip, date(created) as created FROM college.ips'
GET_TOKEN = 'SELECT token FROM college.token WHERE username=\'{username}\''
INSERT = 'INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING id'
UPDATE = 'UPDATE {table} SET {request}'
DELETE = 'DELETE FROM {table} '
IPS_REQUIRED_ATTRS = ['name']
IPS_ALL_ATTRS = ['name', 'id', 'local_ip', 'public_ip', 'created']
IPS_TOOLS_MAIL_ATR = ['mail']

# page str to byte coding
CODING = 'KOI8-R'
