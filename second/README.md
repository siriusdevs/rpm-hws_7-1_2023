## Project description
TODO
## Quick start
### First step: 
- Copy project from git
```
git clone TODO

cd TODO

git checkout nesterov
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
./manage.py drf_create_token -r <username>
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
