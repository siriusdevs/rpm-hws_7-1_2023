# About project:
## It is a simple sever written on python. It uses base python library http.server. Well, BaseHttpServer is a class. I used it to create a custom class which implements CRUD requests. It also used it for realisation REST methods.

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