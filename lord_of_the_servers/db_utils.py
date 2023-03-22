from config import GET_TOKEN, SELECTOR, DELETE, INSERT, UPDATE
from views import list_to_view
from psycopg2 import connect
from psycopg2.errors import UndefinedFunction
from dotenv import load_dotenv
from os import getenv


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


def is_num(value: any):
    return isinstance(value, (int, float))


class DbHandler:

    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def get_data(cls, table: str, req_conds: dict = None) -> dict:
        selector = SELECTOR.format(table=table)
        try:
            cls.db_cursor.execute(DbHandler.query_request(selector, req_conds) if req_conds else selector)
            db_data = cls.db_cursor.fetchall()
        except UndefinedFunction as error:
            db_data = []
            print(f'Database attribute error: {error}')
        return {
            'number': len(db_data),
            f'rendered_{table}s': list_to_view(db_data)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str):
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0] == req_token
        return False

    @staticmethod
    def compose_insert(table: str, insert_data: dict):
        keys = tuple(insert_data.keys())
        values = [insert_data[key] for key in keys]
        attrs = ', '.join(keys)
        values = ', '.join([str(val) if is_num(val) else f"'{val}'" for val in values])
        return INSERT.format(table=table, keys=attrs, values=values)

    @classmethod
    def update(cls, table: str, data: dict, where: dict):
        req = ', '.join([f"{key}={val}" if is_num(val) else f"{key}='{val}'" for key, val in data.items()])
        try:
            cls.db_cursor.execute(cls.query_request(UPDATE.format(table=table, request=req), where))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def insert(cls, table: str, insert_data: dict):
        try:
            cls.db_cursor.execute(cls.compose_insert(table, insert_data))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete(cls, table: str, req_conds: dict):
        try:
            cls.db_cursor.execute(cls.query_request(DELETE.format(table=table), req_conds))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict):
        conditions = []
        for attr, value in req_conds.items():
            to_add = f'{attr}={value}' if isinstance(value, (int, float)) else f"{attr}='{value}'"
            conditions.append(to_add)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))
