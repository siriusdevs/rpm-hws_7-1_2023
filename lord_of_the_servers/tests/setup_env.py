"""Create .env file."""
env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5555',
    'PG_USER': 'test',
    'PG_PASSWORD': 'test',
    'PG_DBNAME': 'test'
}


def setup_env():
    """Set up .env file."""
    lines = [f'{const}={equiv}\n' for const, equiv in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
