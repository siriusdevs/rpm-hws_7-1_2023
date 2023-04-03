# About project:
## It is a simple chat written on python with Flask with registration and authorization.

# How to start
    git clone https://github.com/kirillsev1/SecondPartAtom_hard.git

    git checkout prikhodko

    cd second

    python3.10 -m venv ./venv

    . ./venv/bin/activate

    pip install -r requirements.txt

# Docker container
    docker run -d --name chat -p 5557:5432 \
        -v $HOME/postgresql/chat:/var/lib/postgresql/chat \
        -e POSTGRES_PASSWORD=12345678 \
        -e POSTGRES_USER=chat_user \
        -e POSTGRES_DB=chat_db \
        postgres
### Now run ddl file for creating and filling database
    psql -h 127.0.0.1 -p 5557 -U chat_user chat_db -f init.ddl

### Fill the .env file
### Now move to project directory
### Run server with command:
    python3 -m flask --app app.py run

# Postgres database
## Tables: 
    message fields:
        user_id uuid references chat_user (id),
        filling text

    chat_user fields:
        id uuid primary key not null default uuid_generate_v4(),
        username text,
        email text,
        password text,
        frame_color text

# .env
    HOST - host for http server

    PORT - port for http server

    PG_DBNAME - database name

    PG_HOST - database host

    PG_PORT - database port

    PG_USER - database user

    PG_PASSWORD - database password
    