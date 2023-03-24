"""Init test db."""

from os import getenv

import psycopg2
from dotenv import load_dotenv
load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')
TEST_USER = getenv("TEST_USER")
TEST_TOKEN = getenv("TEST_TOKEN")

if __name__ == '__main__':
    with psycopg2.connect(
            database=PG_DBNAME,
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT) as con:
        cur = con.cursor()
        with open("init.sql", "r") as fi:
            cur.execute(fi.read())

        cur.execute("insert into token values (%s, %s)", (TEST_USER, TEST_TOKEN))
        con.commit()
