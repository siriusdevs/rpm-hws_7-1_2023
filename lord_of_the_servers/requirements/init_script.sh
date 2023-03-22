#!/bin/bash

pip install -r requirements/requirements.txt

# create docker container
docker run -d \
--name book_server \
-p 3850:5432 \
-v $HOME/postgresql/book_server:/var/lib.postgresql/book_server \
-e POSTGRES_PASSWORD=1234 \
-e POSTGRES_USER=app \
-e POSTGRES_DB=book_db \
postgres
sleep 2

# mount all changes
export PGPASSWORD=1234
psql -h 127.0.0.1 -p 3850 -U app book_db -f requirements/db_init.ddl

python3.10 requirements/setup_env.py