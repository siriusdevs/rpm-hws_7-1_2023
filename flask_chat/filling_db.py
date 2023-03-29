"""This file for filling database."""

from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv
from config import EXTENSION, MESSAGE_TABLE, USER_TABLE


load_dotenv()
PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


STEP = [EXTENSION, USER_TABLE, MESSAGE_TABLE]


if __name__ == "__main__":
    with connect(database=PG_DBNAME,
                user=PG_USER,
                password=PG_PASSWORD,
                host=PG_HOST,
                port=PG_PORT) as conn:
        cur = conn.cursor()
        for command in enumerate(STEP):
            cur.execute(command[1])
        conn.commit()
