from config import GET_TOKEN, DELETE, INSERT, UPDATE, SELECTOR
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DBNAME, HOST, PORT, USER, PASSWORD = map(lambda x: getenv(x),
                                         ['PG_DBNAME', 'PG_HOST', 'PG_PORT', 'PG_USER', 'PG_PASSWORD'])


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
            return db_token[0][-37:-1] == req_token
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
            cls.db_cursor.execute(INSERT.format(table='titles', keys='number, phrase', \
                                                values=(DbHandler.find_max_index() + 1, phrase)))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount), DbHandler.find_max_index()

    @classmethod
    def update(cls, data: dict, where: dict):

        colomn, key = list(data.keys())[0], list(where.keys())[0]
        new_value, value = data[colomn], where[key]
        print(UPDATE.format(table='titles', colomn=colomn, new_value=new_value, key=key, value=value))
        try:

            cls.db_cursor.execute(UPDATE.format(table='titles', colomn=colomn,\
                                                new_value=new_value, key=key, value=value))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete(cls, data: dict):
        key = list(data.keys())[0]
        value = data[key]
        try:
            cls.db_cursor.execute(DELETE.format(table='titles', key=key, value=value))
            cls.db_cursor.execute(SELECTOR.format(table='titles'))
            id = value
            for elem in cls.db_cursor.fetchall():
                if elem[0] > value:
                    cls.db_cursor.execute(UPDATE.format(table='titles', colomn='number', \
                                                        new_value=id, key='number', value=elem[0]))
                    id += 1
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        else:
            cls.db_connection.commit()
            return bool(cls.db_cursor.rowcount)
