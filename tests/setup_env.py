env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5555',
    'PG_USER': 'sirius_2023',
    'PG_PASSWORD': 'change_me',
    'PG_DBNAME': 'postgres'
}


def setup_env():
    lines = [f'{const}={value}\n' for const, value in env_consts.items()]
    with open('..env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
