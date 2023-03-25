"""For init test."""

env_consts = {
    'PG_HOST': '127.0.0.1',
    'PG_PORT': '5555',
    'PG_USER': 'test',
    'PG_PASSWORD': 'test',
    'PG_DBNAME': 'test',
    'TEST_USER': 'test',
    "TEST_TOKEN": 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
    "NASA_API": "cDVvENrgh8o5lSHYBFSoX1JRD8kBnT8J98ZLWmbU"
}


def setup_env():
    """Setups env."""
    lines = [f'{const}={valu}\n' for const, valu in env_consts.items()]
    with open('.env', 'w') as env_file:
        env_file.writelines(lines)


if __name__ == '__main__':
    setup_env()
