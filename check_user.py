from faker import Faker
import psycopg2
from os import getenv
from random import choice
def check_passes():
    HOST = getenv("PG_HOST")
    PORT = getenv("PG_PORT")
    USER = getenv("PG_USER")
    PASSWORD = getenv("PG_PASSWORD")
    DBNAME = getenv("PG_DBNAME")
    db_connection = psycopg2.connect(dbname="sirius_2023", host="127.0.0.1", port="38746", user="sirius_2023", password="change_me")
    cursor = db_connection.cursor()
    cursor.execute('select * from users.data;')
    data = {}
    records = cursor.fetchall()
    for row in records:
        data[row[1]] = row[2]
    cursor.close()
    db_connection.close()
    return data