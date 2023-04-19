# server host and port
HOST = '127.0.0.1'
PORT = 8001

# pages
HUMORESKA = '/humoreska'
PAGES = (HUMORESKA)

# templates paths
TEMPLATES = 'templates/'
MAIN_PAGE = '{}index.html'.format(TEMPLATES)
HUMORESKA = '{}humoreska.html'.format(TEMPLATES)
LOGIN = '{}auth.html'.format(TEMPLATES)

# HTTP codes
OK = 200
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400

# db requests
SELECTOR = 'SELECT * FROM students'
GET_TOKEN = 'SELECT token FROM token WHERE username=\'{username}\''
INSERT = 'INSERT INTO group_{group_num} VALUES (\'{name}\')'
DELETE = 'DELETE FROM group_{group_num} WHERE name=\'{name}\''

# page str to byte coding
CODING = 'KOI8-R'

# weather consts
COLLEGE_LOCATION = {'lat': 43.403438, 'lon': 39.981544}
API_URL = 'https://geek-jokes.sameerkumar.website/api?format=json'
