HOST = '127.0.0.1'
PORT = 5000
SECRET_KEY = 'my_secret'

####MESSAGES
USERNAME_TAKEN = 'Username is taken'
MISMATCH = 'Password mismatch'
INCORRECT = "Incorrect password"
NO_SUCH_USERNAME = "There is no such {0}"


######DATABASE
INSERT_MESSAGE = "insert into messages (username, text, time) values (%s, %s, %s)"
SELECT_MESSAGES = 'select * from messages'
SELECT_LAST_MESSAGES = "select * from messages order by time desc limit 50;"
SELECT_SALT_ND_PASSW = "select salt, password from users where username=%s"
REG_USER = "insert into users (username, salt, password) values (%s, %s, %s)"
CHECK_USER = 'select * from users where username=%s'


####FILL DB
EXTENSION = 'create  extension if not exists  \"uuid-ossp\"'

USER_TABLE = 'create table if not exists users (id uuid primary key default uuid_generate_v4(),\
                                                username text not null,\
                                                salt text not null,\
                                                password text not null)'
MESSAGE_TABLE = 'create table if not exists messages (id uuid primary key default uuid_generate_v4(),\
                                                    username text not null,\
                                                    text text not null,\
                                                    time text not null)'

####MAGIC NUMBER
SALT=32
FOR_HASH=10000