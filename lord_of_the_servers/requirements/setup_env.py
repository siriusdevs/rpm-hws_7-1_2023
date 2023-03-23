"""Create .env file."""
env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '3850',
    'PG_USER': 'app',
    'PG_PASSWORD': '1234',
    'PG_DBNAME': 'book_db',
    'API_KEY': '4wI-zjTzFPy5KGT515fT'
}


def setup_env():
    """Set up .env file."""
    lines = [f'{const}={equiv}\n' for const, equiv in env_consts.items()]
    with open('./.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
