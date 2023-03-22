from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv

load_dotenv()
PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')

INSERT_QUOTE = 'insert into quote (author, body) values (%s, %s)'

QUOTES_EXAMPLES = [['Maksim Bezborodov', 'Do you understand? Again you didn\'t understand.'],\
          ['Maksim Bezborodov', 'What does it mean? It means that you are a hole.'],\
          ['Kirill Prikhodko', 'I don\'t understand'],\
          ['siriusdevs', 'ffmpeg is the best'],\
          ['admin', 'алло казлы харош на парах фигнёй страдать']]

QUOTE_TABLE = 'create table if not exists quote\
    (id int primary key generated always as identity,\
    author text not null,\
    body text not null)'

QUOTE_DAY_TABLE = 'create table if not exists quote_day\
    (date text not null primary key,\
    author text not null,\
    body text not null)'

TOKEN_TABLE = 'create table if not exists token\
    (username text not null primary key, token uuid)'

EXTENSION = 'create  extension if not exists  \"uuid-ossp\"'

STEP_1 = [EXTENSION, QUOTE_TABLE, QUOTE_DAY_TABLE, TOKEN_TABLE]

if __name__ == "__main__":
    with connect(database=PG_DBNAME,
                user=PG_USER,
                password=PG_PASSWORD,
                host=PG_HOST,
                port=PG_PORT) as conn:

        cur = conn.cursor()
        for i in range(len(STEP_1)):
            cur.execute(STEP_1[i])
        for quote in QUOTES_EXAMPLES:
            cur.execute(INSERT_QUOTE, (quote[0], quote[1]))
        admin_name = input('Enter your name: ')
        cur.execute('insert into token values (%s, uuid_generate_v4())', (admin_name,))
        conn.commit()
        cur.execute('select username, token from token where username=%s', (admin_name,))
        admin_data = cur.fetchone()
        print(f'Initialization was successful, your superuser credentials:\
              \nADMIN_NAME: {admin_data[0]}\nADMIN_TOKEN: {admin_data[1]}')
