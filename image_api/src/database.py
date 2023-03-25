"""Some functions to work with database."""
from os import getenv

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor

from config import SQL_TOKEN

load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')

db_connection = connect(dbname=PG_DBNAME, host=PG_HOST, port=PG_PORT, user=PG_USER, password=PG_PASSWORD,
                        cursor_factory=RealDictCursor)
db_cursor = db_connection.cursor()


def is_this_user(token: str, user_name: str):
    """Checks if the token belongs to this user.

    Args:
        user_name (str): token owner name.
        token (str): for auth user.
    """
    if check_token(token):
        user, _ = token.split("_")
        return user == user_name
    return False


def check_token(token: str):
    """Checks if token is correct.

    Args:
        token (str): for auth user.
    """
    auth = token.split("_")
    if len(auth) != 2:
        return False
    parameters = "where username = %s"
    db_cursor.execute(SQL_TOKEN.format(parameters=parameters), (auth[0],))
    token_db = db_cursor.fetchone().get("token")
    if not token_db:
        return False

    return auth[1] == token_db
