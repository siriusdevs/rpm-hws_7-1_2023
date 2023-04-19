## Project description
This web application allows you to create a local and public IP entry, view and email a list of data

## Quick start
### First step: 
- Copy project from git
```
git clone https://github.com/nester256/rpm-hws_7-1_2023

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
        -p 38746:5432 \
        postgres:15.1
```
### Third step:
- Create tables
```
psql -h 127.0.0.1 -p 38746 -U admin -d postgres -f db_init.ddl
with password: 1234
```
### Fourth step:
- Create .env file with credentials: 
```
PG_DBNAME=postgres
PG_HOST=127.0.0.1
PG_PORT=38746
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
- In the *Value* field type **admin {'77f498fc-ab20-4017-aa62-c8b246615bae'}**

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
- 