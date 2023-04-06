#!/bin/bash

pip install -r requirements/requirements.txt

# create docker container
docker run -d \
--name fate_server \
-p 3850:5432 \
-v $HOME/postgresql/fate_server:/var/lib.postgresql/fate_server \
-e POSTGRES_PASSWORD=12345F \
-e POSTGRES_USER=app \
-e POSTGRES_DB=phrases_db \
postgres
sleep 2

python3 requirements/setup_env.py

export PGPASSWORD=12345F
psql -h 127.0.0.1 -p 3850 -U app phrases_db -f requirements/db_creator.ddl