# Humoreska

Humoreska is an ultra-safe and nice website with some geek jokes. In order to run it locally, you will need to have Docker desktop and Postgresql installed.

## How to run

To run the app, you should create a Docker container using the following command:

```sh
docker run -d \
--name humoreska \
-e POSTGRES_USER=sirius_2023 \
-e POSTGRES_PASSWORD=change_me \
-e PGDATA=/postgres_data_inside_container \
-v ~/Your/db/path/postgres_data:/postgres_data_inside_container \
-p 38746:5432 \
postgres:15.1
```

You should also log into the database and add your own login and password. Here is an example:

```sql
CREATE EXTENSION "uuid-ossp";

CREATE TABLE IF NOT EXISTS users.data (
   id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
   login text not null,
   pwd text not null
);

INSERT INTO users.data (login, pwd) VALUES (123, 123);
```

Finally, you can run the app using following command:
```
python main.py
```
To make post request to add some users, you should use the following command:
```
Add in headers:
Authorization: q73a3f7-c6c2-4241-8735-1ec2f981b39e
Add in body using json format some data, example below:
{
    "login": "password",
    "login1": "password1",
    "login2": "password2"
}
```
To make delete request to delete some users, you should use the following command:
```
Add in headers:
Authorization: q73a3f7-c6c2-4241-8735-1ec2f981b39e
Add in body using json format some data, example below:
{
    "login": "password",
    "login1": "password1",
    "login2": "password2"
}
```
