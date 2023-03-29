"""File with class for work with DB."""

from psycopg2 import connect
from os import urandom, getenv
from hashlib import pbkdf2_hmac
from datetime import datetime
from config import INSERT_MESSAGE, SELECT_MESSAGES, SELECT_LAST_MESSAGES,\
    REG_USER, CHECK_USER, SELECT_SALT_ND_PASSW, SALT, FOR_HASH
import json
from dotenv import load_dotenv


load_dotenv()
PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


class DBHandler:
    """This class for work with database."""

    connection = connect(database=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)

    @classmethod
    def check_user(cls, username: str):
        """This method if user exists.

        Args:
            username (str): username

        Returns:
            _bool_: result of work.
        """
        with cls.connection.cursor() as cur:
            cur.execute(CHECK_USER, (username,))
            response = cur.fetchone()
            return response is not None

    @classmethod
    def reg_user(cls, username: str, password: str):
        """This method can registration new user.

        Args:
            username (str): username
            password (str): entered password

        Returns:
            _bool_: result of work.
        """
        with cls.connection.cursor() as cur:
            if not DBHandler.check_user(username):
                salt = urandom(SALT)
                passw = pbkdf2_hmac('sha256', password.encode('utf-8'), salt, FOR_HASH)
                cur.execute(REG_USER, (username, salt.hex(), passw.hex()))
                return True
            return False

    @classmethod
    def check_password(cls, username: str, password: str):
        """This method compare password.

        Args:
            username (str): username
            password (str): entered password.

        Returns:
            _bool_: result of work.
        """
        with cls.connection.cursor() as cur:
            cur.execute(SELECT_SALT_ND_PASSW, (username,))
            salt_hex, passw_hex = cur.fetchone()
            salt_db, passw_db = bytes.fromhex(salt_hex), bytes.fromhex(passw_hex)
            check_passw = pbkdf2_hmac('sha256', password.encode('utf-8'), salt_db, FOR_HASH)
            return passw_db == check_passw

    @classmethod
    def send_message(cls, username: str, message: str):
        """This method send message from user.

        Args:
            username (str): username
            message (str): user message.
        """
        with cls.connection.cursor() as cur:
            cur.execute(INSERT_MESSAGE, (username, message, datetime.now().strftime('%H:%M:%S')))

    @classmethod
    def get_messages(cls):
        """This method get all messages.

        Returns:
            json: all messages of chat.
        """
        with cls.connection.cursor() as cur:
            cur.execute(SELECT_MESSAGES)
            response = cur.fetchall()
            return [
                {
                    'id': row[0],
                    'username': row[1],
                    'text': row[2],
                    'time': row[3]
                }
                for row in response
                    ]

    @classmethod
    def get_last_messages(cls):
        """This method get last messages.

        Returns:
            msg_lst(json): json of last messages.
        """
        with cls.connection.cursor() as cur:
            cur.execute(SELECT_LAST_MESSAGES)
            messages = cur.fetchall()
            msg_lst = [
                {
                    'username': message[1],
                    'text': message[2],
                    'time': message[3]
                }
                for message in reversed(messages)
                    ]
            return json.dumps(msg_lst)
