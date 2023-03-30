"""File with database managing class."""
from config import SELECT_ID, SELECT_USERNAME, SELECT_MESSAGE, INSERT_MESSAGE, INSERT_USER, COUNT_USERS, ENDINGS
from psycopg2 import connect
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class DbHandler:
    """Class manages database."""

    connection = connect(
        dbname=getenv('PG_DBNAME'),
        host=getenv('PG_HOST'),
        port=getenv('PG_PORT'),
        user=getenv('PG_USER'),
        password=getenv('PG_PASSWORD')
    )
    cursor = connection.cursor()

    @classmethod
    def get_user_id(cls, username: str, password: str) -> tuple:
        """Method gets user_id by name.

        Args:
            username: str - users name.
            password: str - users password.

        Returns:
            tuple - tuple with id.
        """
        cls.cursor.execute(SELECT_ID, (username, password))
        return cls.cursor.fetchone()

    @classmethod
    def get_username(cls, user_id: str) -> tuple:
        """Method gets username by user_id.

        Args:
            user_id: str - users id(uuid).

        Returns:
            tuple - tuple with username.
        """
        cls.cursor.execute(SELECT_USERNAME, (user_id,))
        return cls.cursor.fetchone()

    @classmethod
    def fill_page(cls):
        """Method gets messages from database.

        Returns:
            tuple - messages from all users.
        """
        cls.cursor.execute(SELECT_MESSAGE)
        return cls.cursor.fetchall()

    @classmethod
    def registrate(cls, username: str, email: str, password: str, frame_color: str) -> None:
        """Method creates new user in database.

        Args:
            username: str - users name.
            email: str - users email.
            password: str - users password.
            frame_color: str - color of filling messages.
        """
        cls.cursor.execute(INSERT_USER, (username, email, password, frame_color))
        cls.connection.commit()

    @classmethod
    def add_massage(cls, message: str, user_id: str) -> None:
        """Method adds new messages into database.

        Args:
            message: str - text from user.
            user_id: str - users id.
        """
        cls.cursor.execute(INSERT_MESSAGE, (user_id, message))
        cls.connection.commit()

    @classmethod
    def check_name(cls, username: str) -> bool:
        """Checks if user exists.

        Args:
            username: str - name of user for checking.

        Returns:
            bool - False if user not in database.
        """
        cls.cursor.execute(COUNT_USERS, (username,))
        return cls.cursor.fetchone()[0] == 0

    @staticmethod
    def check_email(email: str) -> bool:
        """Method checks email.

        Args:
            email: str - users email.

        Returns:
            bool - True if email is valid
        """
        email_arr = []
        for part in email.split('@'):
            if part:
                email_arr.append(part)
        return len(email_arr) > 1 and email.endswith(ENDINGS) and email.count('@') == 1

    @staticmethod
    def check_password(password):
        """Method checks password.

        Args:
            password: str - users password.

        Returns:
            bool - True if password is valid
        """
        return password.isdigit() and len(password) < 5
