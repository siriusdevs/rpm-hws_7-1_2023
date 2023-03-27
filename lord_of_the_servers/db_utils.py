"""Database utilits."""
from config import GET_TOKEN, SELECTOR, DELETE, INSERT, UPDATE, SELECT_ID
from views import list_to_view
from psycopg2 import connect
from dotenv import load_dotenv
from os import getenv
from typing import Any


load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


def is_num(check: Any):
    """Validate whether a variable is a number.

    Args:
        check : any - value for validation
    """
    return isinstance(check, (int, float))


class DbHandler:
    """Handls database requests."""

    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def get_data(cls, table: str, req_conds: dict = None) -> dict:
        """Select data from the table.

        Args:
            table : str - table to search
            req_conds : dict - searching conditions
        """
        selector = SELECTOR.format(table=table)
        try:
            cls.db_cursor.execute(DbHandler.query_request(selector, req_conds) if req_conds else selector)
        except Exception as error:
            db_data = []
            print(f'{__name__} error: {error}')
        else:
            db_data = cls.db_cursor.fetchall()
        return {
            'number': len(db_data),
            f'rendered_{table}s': list_to_view(db_data)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str):
        """Validate admin token.

        Args:
            username : str - name of the user
            req_token : str - needed token
        """
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
            # cls.db_connection.rollback()
        if db_token:
            return db_token[0] == req_token
        return False

    @staticmethod
    def compose_insert(table: str, insert_data: dict):
        """Insert specific values to specific columns.

        Args:
            table : str - table to insert
            insert_data : dict - data to insert
        """
        keys = tuple(insert_data.keys())
        in_values = [insert_data[key] for key in keys]
        attrs = ', '.join(keys)
        in_values = ', '.join([str(in_value) if is_num(in_value) else f"'{in_value}'" for in_value in in_values])
        return INSERT.format(table=table, keys=attrs, values=in_values)

    @classmethod
    def update(cls, table: str, data_to: dict, where: dict):
        """Update specific table.

        Args:
            table : str - table to update
            data_to : dict - data to update
            where : dict - where to update
        """
        req = ', '.join([f"{key}={up_val}" if is_num(up_val) else f"{key}='{up_val}'" for key, up_val in data_to.items()])
        try:
            cls.db_cursor.execute(cls.query_request(UPDATE.format(table=table, request=req), where))
        except Exception as error:
            print(f'{__name__} error: {error}')
            cls.db_connection.rollback()
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def insert(cls, table: str, insert_data: dict):
        """Insert data into specific table.

        Args:
            table : str - table to insert
            insert_data : dict - data to insert
        """
        try:
            cls.db_cursor.execute(cls.compose_insert(table, insert_data))
        except Exception as error:
            print(f'{__name__} error: {error}')
            cls.db_connection.rollback()
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete(cls, table: str, req_conds: dict):
        """Delete data from specific table.

        Args:
            table : str - delete from this table
            req_conds : dict - deletion conditions
        """
        try:
            cls.db_cursor.execute(cls.query_request(DELETE.format(table=table), req_conds))
        except Exception as error:
            print(f'{__name__} error: {error}')
            cls.db_connection.rollback()
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict):
        """Request with conditions.

        Args:
            request : str - request method
            req_conds : dict - conditions of the request
        """
        conditions = []
        for attr, element in req_conds.items():
            to_add = f'{attr}={element}' if isinstance(element, (int, float)) else f"{attr}='{element}'"
            conditions.append(to_add)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))

    @classmethod
    def get_id(cls, table: str, query: dict) -> int:
        """Select id from the table.

        Args:
            table : str - table to search
            query : dict - searching conditions
        """
        try:
            cls.db_cursor.execute(DbHandler.query_request(SELECT_ID.format(table=table), query))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return 0
        return cls.db_cursor.fetchone()[0]
