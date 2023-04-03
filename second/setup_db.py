"""File creates tables in database."""

from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()
creds = {
    "host": getenv("PG_HOST"),
    "port": getenv("PG_PORT"),
    "dbname": getenv("PG_DBNAME"),
    "user": getenv("PG_USER"),
    "password": getenv("PG_PASSWORD"),
}

INIT_FILE = "second/init.ddl"

connection = connect(**creds)
cursor = connection.cursor()
with open(INIT_FILE, 'r') as init_db:
    cursor.execute(init_db.read())

connection.commit()
cursor.close()
connection.close()
