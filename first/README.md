# About project:
## It is a simple sever written on python with http.server. I used BaseHTTPServer class to create a custom example which implements CRUD and REST methods.

# How to start
    git clone https://github.com/kirillsev1/SecondPartAtom_hard.git

    git checkout prikhodko

    cd first

    python3.10 -m venv ./venv

    . ./venv/bin/activate

    pip install -r requirements.txt

# Docker container
    docker run -d --name library_project_7_1 -p 5435:5432 \
        -v $HOME/postgresql/http_db:/var/lib/postgresql/http_db \
        -e POSTGRES_PASSWORD=12345678 \
        -e POSTGRES_USER=app \
        -e POSTGRES_DB=http_db \
        postgres
### Now run ddl file for creating and filling database
    psql -h 127.0.0.1 -p 5435 -U app http_db -f init_db.ddl

### Finally, fill the .env file

# GET POST PUT UPDATE
## Server requests(CRUD) could be sent for example from Postman, but to send a right request there must be a username and token from database because of authentication:  
### For example to PUT, POST or UPDATE database data the body raw must be filled:
    {"fname": "Kirill", "lname": "Prikhodko", "email": "email1@email.com"}
### It should be used with url field parameters from .env file:
    HOST:PORT(127.0.0.1:8000)

### For DELETE request url field must be filled with parameters after HOST:PORT and ?;
    127.0.0.1:8000/?fname=Kirill&lname=Prikhodko

# Postgres database
## Tables: 
    token fields:
        username text primary key, 
        token uuid

    people fields:
        id integer generated always as identity not null primary key, 
        fname text not null, 
        lname text not null, 
        fname text, 
        email text not null

# .env
    HOST - host for http server

    PORT - port for http server

    PG_DBNAME - database name

    PG_HOST - database host

    PG_PORT - database port

    PG_USER - database user

    PG_PASSWORD - database password
    
    TEMPLATES_FILE