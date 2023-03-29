"""File with configuration data."""
# templates
INDEX_TEMPLATE = 'index.html'
CHAT_TEMPLATE = 'chat.html'
LOGIN_TEMPLATE = 'login.html'
REG_TEMPLATE = 'registration.html'

# errors
USERNAME_ERROR = 'Username already exists or too long'
PASSWORD_ERROR = 'Incorrect password'
EMAIL_ERROR = 'Incorrect email'
LOGIN_ERROR = 'Check your password and username'

# paths
INDEX_PATH = '/'
CHAT_PATH = '/chat'
LOGIN_PATH = '/login'
REG_PATH = '/registration'
LOGOUT_PATH = '/logout'

# DB requests
SELECT_ID = 'select id from chat_user where username=%s and password=%s'
SELECT_USERNAME = 'select username from chat_user where id=%s'
SELECT_MESSAGE = 'select username, filling, frame_color from message join chat_user on chat_user.id=user_id'
INSERT_USER = 'insert into chat_user (username, email, password, frame_color) values (%s, %s, %s, %s)'
INSERT_MESSAGE = 'insert into message (user_id, filling) values (%s, %s)'
COUNT_USERS = 'select count(username) from chat_user where username=%s'


# other
COLORS = ('#B6DCEE', '#91ECF1', '#89F8D5', '#B4FEA3', '#F9F871')
ENDINGS = ('.ru', '.com')
MAX_NAME_LEN = 30
