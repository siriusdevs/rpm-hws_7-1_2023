from http.server import HTTPServer
from os import getenv
import psycopg2
from config import HOST, PORT
from http_handler import CustomHandler

if __name__ == '__main__':
    try:
        db_connection = psycopg2.connect(
        dbname=getenv("PG_DBNAME"),
        host=getenv("PG_HOST"),
        port=getenv("PG_PORT"), user=getenv("PG_USER"),
        password=getenv("PG_PASSWORD"),
        )
        cursor = db_connection.cursor()
    except psycopg2.OperationalError:
        print("Не подключена база данных")
    else:
        with HTTPServer((HOST, PORT), CustomHandler) as server:
            server.serve_forever()
