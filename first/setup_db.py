
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

FILE = "db_init.ddl"

connection = connect(**creds)
cursor = connection.cursor()
with open(FILE, 'r') as file:
    cursor.execute(file.read())


connection.commit()
cursor.close()
connection.close()