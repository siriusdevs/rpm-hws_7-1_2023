import psycopg2
from os import getenv


def check_passes():
    db_connection = psycopg2.connect(dbname=getenv("PG_DBNAME"), host=getenv("PG_HOST"),
                                    port=getenv("PG_PORT"), user=getenv("PG_USER"),
                                    password=getenv("PG_PASSWORD"))
    cursor = db_connection.cursor()
    cursor.execute('select * from users.data;')
    data = {}
    records = cursor.fetchall()
    for row in records:
        data[row[1]] = row[2]
    cursor.close()
    db_connection.close()
    return data
