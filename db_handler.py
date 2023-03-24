from config import GET_TOKEN, DELETE, INSERT, UPDATE, SELECTOR, LEN_UUID
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DBNAME = getenv('PG_DBNAME')
HOST = getenv('PG_HOST')
PORT = getenv('PG_PORT')
USER = getenv('PG_USER')
PASSWORD = getenv('PG_PASSWORD')


class DbHandler:

    db_connection = connect(dbname=DBNAME, host=HOST, port=PORT, user=USER, password=PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def find_max_index(cls):
        max_ind = 1
        cls.db_cursor.execute('select number from titles;')
        for elem in cls.db_cursor.fetchall():
            if elem[0] > max_ind:
                max_ind = elem[0]
        return max_ind

    @classmethod
    def is_valid_token(cls, username: str, req_token: str):
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0][LEN_UUID:-1] == req_token
        return False

    @classmethod
    def get_data(cls) -> list:
        cls.db_cursor.execute(SELECTOR.format(table='titles'))
        res = []
        for elem in cls.db_cursor.fetchall():
            res.append(elem[1])
        return res

    @classmethod
    def insert(cls, insert_data: dict):
        try:
            phrase = insert_data['phrase']
        except Exception:
            print("No key 'phrase' in data")
            return False
        value = DbHandler.find_max_index() + 1
        try:
            cls.db_cursor.execute(INSERT.format(table='titles', keys='number, phrase', values=(value, phrase)))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount), cls.find_max_index()

    @classmethod
    def update(cls, data: dict, where: dict):

        colomn, key = list(data.keys())[0], list(where.keys())[0]
        new_value, value = data[colomn], where[key]
        print(UPDATE.format(table='titles', colomn=colomn, new_value=new_value, key=key, value=value))
        try:

            cls.db_cursor.execute(UPDATE.format(table='titles', colomn=colomn, new_value=new_value, key=key, value=value))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete_and_change(cls, key, value):
        cls.db_cursor.execute(DELETE.format(table='titles', key=key, value=value))
        cls.db_cursor.execute(SELECTOR.format(table='titles'))
        ident = value
        for elem in cls.db_cursor.fetchall():
            if elem[0] > value:
                cls.db_cursor.execute(UPDATE.format(table='titles', colomn='number', new_value=ident, key='number', value=elem[0]))
                ident += 1

    @classmethod
    def delete(cls, data: dict):
        key = list(data.keys())[0]
        value = data[key]
        try:
            cls.delete_and_change(key, value)
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)
