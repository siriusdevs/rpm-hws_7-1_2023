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
    docker run -d --name python_server -p 5435:5432 \
        -v $HOME/postgresql/http_db:/var/lib/postgresql/http_db \
        -e POSTGRES_PASSWORD=12345678 \
        -e POSTGRES_USER=app \
        -e POSTGRES_DB=http_db \
        postgres
### Now run ddl file for creating and filling database
    psql -h 127.0.0.1 -p 5435 -U app http_db -f init.ddl

### Fill the .env file
### Now move to project directory
### Run server with command:
    python3 main.py

# GET POST PUT UPDATE
## Server requests(CRUD) could be sent for example from Postman, but to send a right request there must be a username and token from database because of authentication:  
### Token locates in database. So, select it from table:
    psql -h 127.0.0.1 -p 5435 -U app http_db - [Connection to database]
    enter password: - [POSTGRES_PASSWORD=12345678]
    SELECT * FROM token; - [User and token]
### Now put it into Postman headers(Authorization token):
    ------------------------------------
    |  Authorization   |  user{token}  |
    ------------------------------------
    
    --------------------------------------------------------------------
    |  Authorization   |  admin{a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3}  |
    --------------------------------------------------------------------
### Example for PUT, POST or UPDATE database data the body raw must be filled:
    {"fname": "Kirill", "lname": "Prikhodko", "email": "email1@email.com"}
### It should be used with url field parameters from .env file:
    HOST:PORT(127.0.0.1:8000)
### Results of requests are situated in main page. There you can find posted persons by using filter:
    127.0.0.1:8000/?fname=Kirill
### For DELETE request url field must be filled with parameters after HOST:PORT and ?;
    127.0.0.1:8000/main?fname=Kirill&lname=Prikhodko
### If DELETE query was right there won't be information about person.
### Track also may occur with database. Connect to it and select information from people table:
    psql -h 127.0.0.1 -p 5435 -U app http_db - [Connection to database]
    enter password: - [POSTGRES_PASSWORD=12345678]
    SELECT * FROM people;

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
    
    TEMPLATES_PATH - path to templates directory 