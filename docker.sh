docker run -d \
--name mars_project \
-e POSTGRES_USER=admin \
-e POSTGRES_PASSWORD=admin \
-e PGDATA=/postgres_data_inside_container \
-v /Users/nirtkor/sirius_db_2023/postgres_data \
-p 38746:5432 \
postgres:15.1