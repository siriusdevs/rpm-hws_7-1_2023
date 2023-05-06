## Project description
TODO
## Quick start
### First step: 
- Copy project from git
```
git clone https://github.com/nester256/rpm-hws_7-1_2023

cd rpm-hws_7-1_2023

git checkout nesterov

cd second
```
### Second step:
- Create docker image 
```
docker run  -d \
        --name restaurants_test \
        -e POSTGRES_USER=admin \
        -e POSTGRES_PASSWORD=1234 \
        -e PGDATA=/postgres_data \
        -v ~/djangoproject_hw2/postgres_data:/postgres_data \
        -p 38746:5432 \
        postgres:15.1
```
### Third step:
```
./manage.py migrate

./manage.py createsuperuser
<Enther username>

./manage.py drf_create_token -r <username>
```
### Fourth step:
- Create .env file with credentials: 
```
PG_DBNAME=restaurants_test
PG_HOST=127.0.0.1
PG_PORT=38746
PG_USER=admin
PG_PASSWORD=1234
```
### Finally
- Run server
```
./manage.py runserver
```
- And see what`s in there by going to: http://127.0.0.1:8000/main_page/

## TODO URL to create location
http://dimik.github.io/ymaps/examples/location-tool/1

## HTTP Requests with Postman
### For sending PUT, POST and DELETE requests to the databases you must be an authorized user

#### Go to Postman and add:

In the url add:
- http://127.0.0.1:8000/update_place/

In the tab **Headers**:
- In the *Key* field type **Authorization**
- In the *Value* field type **Token created token in Third step **
![Example for add token](image_url)

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
