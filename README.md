## Project description
This web application allows you to create a local and public IP entry, view and email a list of data

## Quick start
### First step: 
- Copy project from git
```
git clone git clone https://github.com/nester256/rpm-hws_7-1_2023/tree/nesterov

cd rpm-hws_7-1_2023

git checkout nesterov
```
### Second step:
- Create docker image 
```
docker run  -d \
        --name ips_test \
        -e POSTGRES_USER=admin \
        -e POSTGRES_PASSWORD=1234 \
        -e PGDATA=/postgres_data_inside_container \
        -v ~/sirius_db_2023/postgres_data:/postgres_data_inside_container \
        -p 38746:5432 \
        postgres:15.1
```
### Third step:
- Create tables
```
psql -h 127.0.0.1 -p 5435 -u admin ips_tests -f db_init.ddl
```
### Fourth step:
- Create .env file with credentials: 
```
PG_DBNAME=postgres
PG_HOST=127.0.0.1
PG_PORT=5432
PG_USER=admin
PG_PASSWORD=1234
(optional, for test doesn`t need)
SMTP_MAIL=***
SMTP_MAIL_PASSWORD=***
```
### Finally
- Run server
```
python3.X main.py
```
- And see what`s in there by going to: http://127.0.0.1:8001/


## HTTP Requests with Postman
### For sending PUT, POST and DELETE requests to the databases you must be an authorized user
Go to Postman and add:
In the tab **Headers**:
- In the *Key* field type **Authorization**
- In the *Value* field type **admin {token}**
To find out your token:
```
psql -h 127.0.0.1 -p 5435 -u admin ips_tests

SELECT token FROM token WHERE username="admin"
```

### If you want to execute POST, PUT requests

#### For add ip (POST)
- In *URL* field: http://127.0.0.1:8001/ips
- In *Body* tab: input raw JSON
**Example**: {"name": "home345678"}

#### For update ip (PUT)
- In *URL* field: http://127.0.0.1:8001/ips?id=1
- In *Body* tab: input raw JSON
**Example**: {"name": "home345678", "public_ip": "228.228.228.255"}

#### If you want to execute DELETE requests
- In *URL* field: http://127.0.0.1:8001/ips?
- After **"?"** you specify what data you want to delete
**Example**: http://127.0.0.1:8001/ips?id=1
