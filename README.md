Ultra safe and nice website with some geek jokes.

Requirements:
    Docker desktop,
    Postgresql

To run it by your own you shold make an docker container using:

_$docker run  -d \                     
_$       --name humoreska \
_$        -e POSTGRES_USER=sirius_2023 \
_$        -e POSTGRES_PASSWORD=change_me \
_$        -e PGDATA=/postgres_data_inside_container \
_$        -v ~/ Your db path /postgres_data:/postgres_data_inside_container \
_$        -p 38746:5432 \
_$        postgres:15.1"

Also you need to log into db and add some login and passwords into db. For example:

_$CREATE TABLE IF NOT EXISTS users.data 
_$(
_$    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
_$    login text not null,
_$    pwd text not null
_$);"

_$INSERT INTO users.data (login, pwd) VALUES (123, 123);

After that you can run app using main.py
