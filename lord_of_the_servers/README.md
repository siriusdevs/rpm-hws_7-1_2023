# Getting Started!
## Initialization and installation
Execute the following commands to prepare for the start:
```
git clone https://github.com/annashutova/rpm-hws_7-1_2023

git checkout shutova

cd lord_of_the_servers
```

The next step is:
```
python3 init.py
```
This command will install all the requirements for the project, like: moduls, docker container, database, .env file.

In the terminal you will see the following line:
```
See file "requirements/authorization.txt" for database authorization info
```
This file containes authorization information for HTTP requests. *(See topic below)*

## Run server
You can run the server with the following command:
```
python3 main.py
```

And see what`s in there by going to:
    http://127.0.0.1:8002/

## HTTP Requests with Posstman
### For sending PUT, POST and DELETE requests to the databases you must be an authorized user
Go to Postman and add:
In the tab **Headers**:
- In the *Key* field type **Authorization**
- In the *Value* field type **admin {token}**
Your token is in the *requirements/authorization.txt*

### If you want to execute POST, PUT requests

#### For Books
- In *URL* field: http://127.0.0.1:8002/book
- In *Body* tab: input raw JSON
**Example**: {"title": "some book title", "volume": 1, "published": 2000}

#### For Movies
- In *URL* field: http://127.0.0.1:8002/movie
- In *Body* tab: input raw JSON
**Example**: {"title": "some movie title", "duration": 160, "released": 2000}

### If you want to execute DELETE requests
- In *URL* field: http://127.0.0.1:8002/book
- After **"?"** you specify what data you want to delete
**Example**: http://127.0.0.1:8002/book?title=Book&volume=30
*The same goes with the movies but you replace "/book" with "/movie" in the URL*