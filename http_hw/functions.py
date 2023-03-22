"""Classes for api requests."""


from config import *
from psycopg2 import connect
from datetime import datetime
import requests
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException


load_dotenv()
PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


class NotFoundException(HTTPException):
    """Custom exception for 404 code."""

    def __init__(self):
        """Returns code and message."""
        super().__init__(status_code=NOT_FOUND['code'], detail=NOT_FOUND)


class BadRequestException(HTTPException):
    """Custom exception for 400 code."""

    def __init__(self):
        """Returns code and message."""
        super().__init__(status_code=BAD_REQUEST['code'], detail=BAD_REQUEST)


class ForbiddenException(HTTPException):
    """Custom exception for 403 code."""

    def __init__(self):
        """Returns code and message."""
        super().__init__(status_code=FORBIDDEN['code'], detail=FORBIDDEN)


class DBHandler():
    """Class for work with database."""

    conn = connect(database=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    cur = conn.cursor()

    @classmethod
    def check_auth(cls, token):
        """Method that checks token for valid.

        Args:
            token (str): user token

        Raises:
            ForbiddenException: raises if token invalid

        Returns:
            bool: result of work.
        """
        token = str(token).split()
        with cls.conn.cursor() as cur:
            cur.execute(SELECT_TOKEN, (token[0],))
            response = cur.fetchone()
            if response:
                response = '{0}{1}{2}'.format('{', str(response[0]), '}')
                if token[1] == response:
                    return True
                raise ForbiddenException
            raise ForbiddenException

    @staticmethod
    def get_with_id(cur, id):
        """Method that get quote with id.

        Args:
            cur (psycopg2.extensions.cursor): cursor db.
            id (int): quote id

        Returns:
            dict: result of work.
        """
        cur.execute(GET, (id,))
        response = cur.fetchall()
        return [{'id': elem[0], 'author': elem[1], 'body': elem[2]} for elem in response]

    @staticmethod
    def check(cur, select, author, body=None):
        """Check infromatin about author.

        Args:
            cur (psycopg2.extensions.cursor): cursor of db
            select (str): command for db
            author (str): quote author
            body (str): quote body. Defaults to None.

        Returns:
            bool: result of work.
        """
        cur.execute(select, (author,))
        response = cur.fetchall()
        if not response:
            return False
        data_lst = [elem[0] for elem in response]
        if body:
            return body not in data_lst
        return author in data_lst

    @staticmethod
    def check_get(cur, author, body):
        """Method check something.

        Args:
            cur (psycopg2.extensions.cursor): cursor of db
            author (str): quote author
            body (str): quote body

        Returns:
            dict: result of work
        """
        if DBHandler.get_authors(cur, author):
            return DBHandler.check(cur, POST_SELECT, author, body)
        return True

    @classmethod
    def process_post(cls, author: str, body: str) -> dict:
        """Method that posts new quote.

        Args:
            author (str): quote author
            body (str): quote body

        Raises:
            BadRequestException: raises if body exists

        Returns:
            dict: result of work
        """
        with cls.conn.cursor() as cur:
            if cls.check_get(cur, author, body):
                cur.execute(INSERT, (author, body))
                cls.conn.commit()
                cur.execute(SELECT_ID, (author, body))
                POST_OK["url"] = "http://{0}:{1}/quotes?id={2}".format(HOST, PORT, cur.fetchone()[0])
                return POST_OK
            raise BadRequestException

    @classmethod
    def process_put(cls, author, body, id):
        """Method that put new data in quote.

        Args:
            author (str): author name
            body (str): quote body
            id (int): quote body

        Raises:
            NotFoundException: raises if id not found

        Returns:
            dict: result of work.
        """
        with cls.conn.cursor() as cur:
            if not cls.check(cur, GET, id):
                raise NotFoundException
            cur.execute(UPDATE, (author, body, id))
            cls.conn.commit()
            return PUT_OK

    @classmethod
    def process_delete(cls, id: int):
        """Method that deletes quote.

        Args:
            id (int): quote id

        Raises:
            NotFoundException: raises if id not found

        Returns:
            dict: result of work
        """
        with cls.conn.cursor() as cur:
            if not cls.check(cur, GET, id):
                raise NotFoundException
            cur.execute(DELETE, (id,))
            cls.conn.commit()
            return DELETE_OK

    @staticmethod
    def get_authors(cur, author):
        """Method that all authors.

        Args:
            cur (psycopg2.extensions.cursor): _description_
            author (str): _description_

        Returns:
            dict: authors
        """
        cur.execute(GET_ALL_AUTHORS)
        authors = cur.fetchall()
        auth_lst = [author[0] for author in authors]
        return author in auth_lst

    @classmethod
    def process_get(cls, author: str = None, id: int = None):
        """Method that return author.

        Args:
            author (str): quote author. Defaults to None.
            id (int): quote id. Defaults to None.

        Raises:
            NotFoundException: raises if author or id not found.

        Returns:
            dict: quotes
        """
        with cls.conn.cursor() as cur:
            if author:
                if not cls.get_authors(cur, author):
                    raise NotFoundException
                cur.execute(GET_AUTHOR, (author,))
                response = cur.fetchall()
                return [{'id': elem[0], 'author': elem[1], 'body': elem[2]} for elem in response]
            if id:
                if not cls.check(cur, GET, id):
                    raise NotFoundException
                return cls.get_with_id(cur, id)

    @classmethod
    def select_quotes(cls):
        """Method that return all quotes.

        Returns:
            dict: all quotes
        """
        with cls.conn.cursor() as cur:
            cur.execute(SELECTOR)
            response = cur.fetchall()
            return [{'id': elem[0], 'author': elem[1], 'body': elem[2]} for elem in response]

    @classmethod
    def process_day(cls):
        """Method that return quote of day.

        Returns:
            dict: quote
        """
        with cls.conn.cursor() as cur:
            cur.execute(DATE_SELECTOR)
            response = cur.fetchall()
            date_lst = [quote_item[0] for quote_item in response]
            date_now = datetime.datetime.now().strftime('%m-%d-%Y')

            if date_now in date_lst:
                cur.execute(DAY_SELECTOR, (date_now,))
                day_q = cur.fetchall()[0]
                return {"author": f"{day_q[0]}", "body": f"{day_q[1]}"}

            response = requests.get(URL, headers=HEADERS)
            day_q = response.json()['quote']
            cur.execute(DAY_INSERT, (datetime.now().strftime('%m-%d-%Y'), day_q['author'], day_q['body']))
            cls.conn.commit()
            return day_q
