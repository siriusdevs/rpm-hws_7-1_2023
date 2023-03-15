"""File with database managing utils."""
from config import SELECTOR, GET_TOKEN, INSERT, UPDATE, DELETE, FIRST_LINE, TABLE
from view import is_num, list_to_view
from dotenv import load_dotenv
from psycopg2 import connect
from os import getenv

load_dotenv()

PG_DBNAME = getenv("PG_DBNAME")
PG_HOST = getenv("PG_HOST")
PG_PORT = getenv("PG_PORT")
PG_USER = getenv("PG_USER")
PG_PASSWORD = getenv("PG_PASSWORD")


class DbHandler:
    """Class which sends queries to database."""

    db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD)
    db_cursor = db_connection.cursor()

    @classmethod
    def remove_data(cls) -> None:
        """Method removes all data from table."""
        cls.db_cursor.execute(FIRST_LINE.format(table=TABLE))
        if not cls.db_cursor.fetchone():
            return
        cls.db_cursor.execute("DELETE FROM people")

    @classmethod
    def get_data(cls, req_conds: dict = None) -> dict:
        """Method gets all data from table.

        Args:
            req_conds: dict - params for selection.

        Returns:
            dict - dict with number of lines in table and list of table lines.
        """
        cls.db_cursor.execute(DbHandler.query_request(SELECTOR, req_conds) if req_conds else SELECTOR)
        selection = cls.db_cursor.fetchall()
        print(selection)
        return {
            'number': len(selection),
            'rendered_people': list_to_view(selection)
        }

    @classmethod
    def is_valid_token(cls, username: str, req_token: str) -> bool:
        """Method checks token in CRUD requests.

        Args:
            username: str - name for auth.
            req_token: str - user token.
        """
        cls.db_cursor.execute(GET_TOKEN.format(username=username))
        db_token = cls.db_cursor.fetchone()
        if db_token:
            return db_token[0] == req_token
        return False

    @staticmethod
    def compose_insert(insert_data: dict) -> str:
        """Method creates insert request.

        Args:
            insert_data: dict - attrs for insert.

        Returns:
            str - insert request with params_values and data.
        """
        keys = tuple(insert_data.keys())
        params_values = [insert_data[key] for key in keys]
        attrs = ', '.join(keys)
        params_values = ', '.join(
            [str(params_val) if is_num(params_val) else f"'{params_val}'" for params_val in params_values]
        )
        return INSERT.format(table='people', keys=attrs, values=params_values)

    @classmethod
    def update(cls, record: dict, where: dict) -> bool:
        """Method updates data in database.

        Args:
            record: dict - new data for post request.
            where: dict - dict of params by which method updates data.

        Returns:
            bool - returns True if post finished successfully.
        """
        req = ', '.join(
            [f"{key}={key_val}" if is_num(key_val) else f"{key}='{key_val}'" for key, key_val in record.items()]
        )
        try:
            cls.db_cursor.execute(cls.query_request(UPDATE.format(table='people', request=req), where))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def insert(cls, people_data: dict) -> bool:
        """Method which tries to send insert request.

        Args:
            people_data: dict - insert data.

        Returns:
            bool - returns True if insert finished successfully.
        """
        try:
            cls.db_cursor.execute(cls.compose_insert(people_data))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @classmethod
    def delete(cls, req_conds: dict) -> bool:
        """Method which tries to remove data from table.

        Args:
            req_conds: dict - attrs by which method will find what to delete.

        Returns:
              bool - returns True if delete finished successfully.
        """
        try:
            cls.db_cursor.execute(cls.query_request(DELETE.format(table=TABLE), req_conds))
        except Exception as error:
            print(f'{__name__} error: {error}')
            return False
        cls.db_connection.commit()
        return bool(cls.db_cursor.rowcount)

    @staticmethod
    def query_request(request: str, req_conds: dict) -> str:
        """Method adds into request selection conds.

        Args:
            request: str - method post, delete or insert.
            req_conds: dict - dict of conditions for request.

        Returns:
            str - request with conditions.
        """
        conditions = []
        for attr, attr_val in req_conds.items():
            to_add = f'{attr}={attr_val}' if isinstance(attr_val, (int, float)) else f"{attr}='{attr_val}'"
            conditions.append(to_add)
        print(conditions)
        return '{0} WHERE {1}'.format(request, ' AND '.join(conditions))
