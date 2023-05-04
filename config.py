# server host and port
HOST = '127.0.0.1'
PORT = 8001

# pages
HUMORESKA = '/humoreska'
PAGES = (HUMORESKA)

# templates paths
TEMPLATES = 'templates/'
MAIN_PAGE = '{0}index.html'.format(TEMPLATES)
HUMORESKA = '{0}humoreska.html'.format(TEMPLATES)
LOGIN = '{0}auth.html'.format(TEMPLATES)

# HTTP codes
OK = 200
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

# page str to byte coding
CODING = 'KOI8-R'

API_URL = 'https://geek-jokes.sameerkumar.website/api?format=json'
