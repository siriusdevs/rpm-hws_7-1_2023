Ultra safe and nice website with some geek jokes.

Requirements:
    Docker desktop
    Postgresql

To run it by your own you shold make an docker container using:

docker run  -d \                     
        --name humoreska \
        -e POSTGRES_USER=sirius_2023 \
        -e POSTGRES_PASSWORD=change_me \
        -e PGDATA=/postgres_data_inside_container \
        -v ~/<Your db path>/postgres_data:/postgres_data_inside_container \
        -p 38746:5432 \
        postgres:15.1

Also you need to log into db and add some login and passwords into db. For example:

CREATE TABLE IF NOT EXISTS users.data 
(
    id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
    login text not null,
    pwd text not null
);

INSERT INTO users.data (login, pwd) VALUES (123, 123);

After that you can run app using main.py
