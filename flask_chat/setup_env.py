"""File that setup env."""

env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5439',
    'PG_USER': 'user',
    'PG_PASSWORD': '123456',
    'PG_DBNAME': 'chat'
}


def setup_env():
    """This function create file .env with consts."""
    lines = [f'{const}={itemm}\n' for const, itemm in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
