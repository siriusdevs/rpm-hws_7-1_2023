""" Модуль содержит методы для работы с pSQL. """
import psycopg2
from os import getenv
from dotenv import load_dotenv
from psycopg2 import errors

load_dotenv()

PG_DBNAME = getenv('PG_DBNAME')
PG_HOST = getenv('PG_HOST')
PG_PORT = getenv('PG_PORT')
PG_USER = getenv('PG_USER')
PG_PASSWORD = getenv('PG_PASSWORD')


def register_user(username, password):
    
    """
    Регистрация нового пользователя в базе данных.
    Args:
        username: Имя пользователя.
        password: Пароль пользователя.
    """
    conn = psycopg2.connect(
        database=PG_DBNAME,
        user=PG_USER,
        password=PG_PASSWORD,
        host=PG_HOST,
        port=PG_PORT
    )
    cur = conn.cursor()

    cur.execute(
        'CREATE TABLE IF NOT EXISTS users ('
        '    id SERIAL PRIMARY KEY,'
        '    username VARCHAR(255) NOT NULL,'
        '    password VARCHAR(255) NOT NULL'
        ');'
    )

    cur.execute(
        'INSERT INTO users (username, password) VALUES (%s, %s);',
        (username, password)
    )

    conn.commit()

    cur.close()
    conn.close()


def check_credentials(username, password):
    """
    Проверка учетных данных пользователя.
    :param username: Имя пользователя.
    :param password: Пароль пользователя.
    :return: True, если учетные данные верные, иначе False.
    """
    conn = psycopg2.connect(database=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM users WHERE username = %s AND password = %s;
    """, (username, password))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user is not None


def create_history_table():
    """
    Создание таблицы истории запросов.
    """
    try:
        conn = psycopg2.connect(dbname=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS user_history (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                sol INT NOT NULL,
                timestamp TIMESTAMP NOT NULL DEFAULT NOW()
            );
        ''')
        conn.commit()
    except errors.Error as e:
        print(f"Unable to create table: {e}")
    finally:
        if conn:
            conn.close()


def save_sol(user_id, sol):
    """
    Сохранение запроса на вывод изображения в историю.
    :param user_id: Идентификатор пользователя.
    :param sol: Значение sol.
    """
    try:
        conn = psycopg2.connect(dbname=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
        cur = conn.cursor()

        cur.execute(
            'INSERT INTO user_history (user_id, sol) VALUES (%s, %s);',
            (user_id, sol,)
        )
        conn.commit()
    except errors.Error as e:
        print(f"Unable to save sol: {e}")
    finally:
        if conn:
            conn.close()


def get_user_history(username):
    """
    Получение истории запросов пользователя.
    :param username: Имя пользователя.
    :return: Список словарей с данными о запросах.
    """
    with psycopg2.connect(dbname=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT sol, timestamp FROM user_history WHERE user_id = %s", (username,))
            return [{'sol': row[0], 'timestamp': row[1].strftime("%Y-%m-%d %H:%M:%S")} for row in cur.fetchall()]


def delete_user(username):
    """
    Удаление пользователя из базы данных.
    :param username: Имя пользователя.
    """
    conn = psycopg2.connect(database=PG_DBNAME, user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)
    cur = conn.cursor()

    cur.execute("""
    DELETE FROM users WHERE username = %s;
    """, (username,))
    
    cur.execute("""
    DELETE FROM user_history WHERE user_id = %s;
    """, (username,))

    conn.commit()

    cur.close()
    conn.close()
