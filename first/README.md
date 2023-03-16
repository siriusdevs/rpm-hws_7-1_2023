# About project:
## It is a simple sever written on python with http.server. I used BaseHTTPServer class to create a custom example which implements CRUD and REST methods.

# How to start
    git clone https://github.com/kirillsev1/SecondPartAtom_hard.git

    git checkout prikhodko

    cd first

    python3.10 -m venv ./venv

    . ./venv/bin/activate

    pip install -r requirements.txt

# GET POST PUT UPDATE
## Server requests(CRUD) could be sent for example from Postman, but to send a right request there must be a username and token from database because of authentication:  
### For example to PUT, POST or UPDATE database data the body raw must be filled:
    {"fname": "Kirill", "lname": "Prikhodko", "email": "email1@email.com"}
### It should be used with url field parameters from .env file:
    HOST:PORT(127.0.0.1:8000)

### For DELETE request url field must be filled with parameters after HOST:PORT and ?;
    127.0.0.1:8000/?fname=Kirill&lname=Prikhodko

# this server needs:

## postgres database
##### with tables: 
##### token (username text primary key, token uuid)
##### people (id integer generated always as identity not null primary key, fname text not null, lname text not null, fname text, email text not null)

# .env
#### HOST - host for http server

#### PORT - port for http server

#### PG_DBNAME - database name

#### PG_HOST - database host

#### PG_PORT - database port

#### PG_USER - database user

#### PG_PASSWORD - database password

#### API_KEY - API key from token table

#### USER_API - API user from token table