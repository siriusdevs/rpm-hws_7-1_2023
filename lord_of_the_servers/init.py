import os
import stat
from psycopg2 import connect
from dotenv import load_dotenv


FILE = 'requirements/init_script.sh'
OUTPUT_FILE = 'requirements/authorization.txt'


def run_container():
    st = os.stat(FILE)
    os.chmod(FILE, st.st_mode | stat.S_IEXEC)
    os.system(f'./{FILE}')


def load_token():
    # load .env variables
    load_dotenv()
    PG_DBNAME = os.getenv('PG_DBNAME')
    PG_HOST = os.getenv('PG_HOST')
    PG_PORT = os.getenv('PG_PORT')
    PG_USER = os.getenv('PG_USER')
    PG_PASSWORD = os.getenv('PG_PASSWORD')

    # get admin token from database
    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()
    db_cursor.execute("SELECT token FROM token where username='admin'")
    token = db_cursor.fetchone()
    db_cursor.close()
    db_connection.close()
    with open(OUTPUT_FILE, 'wt') as user_inf:
        user_inf.write(f'AUTH DATABASE INFO:\nusername: admin\ntoken: {token[0]}')
    print(f'See file "{OUTPUT_FILE}" for database authorization info')


if __name__ == '__main__':
    run_container()
    load_token()