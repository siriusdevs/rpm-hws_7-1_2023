# Project starts up FastAPI server, which can take data from anilist and do REST API on your own server.

# How install
_$ sudo apt-get update_

_$ docker pull mongo_

_$ git clone https://github.com/Max2288/rpm-hws_7-1_2023/_


# How run
Add .env file with your data

Go to repo/flask and run commands:

_$ docker run -d -p 27018:27017 --name test_shop mongo_

_$ python3.10 -m venv ./venv_

_$ . ./venv/bin/activate_

_$ pip install -r requirements.txt_

# After start


## POST request

You can post media on page / (Postman recommended)

* Go to Postman
* Query example: _http://HOST:5000/index/create


Example of data that we send to post: 

    {
        "id": int,
        "source_to_img" : str (path in static images),
        "name" : str,
        "price" : float | int,
        "description" : str,
        "featured_products" : bool
    }

## PUT request

You can update media on page / (Postman recommended)

* Go to Postman
* Query example: _http://HOST:5000//index/update


Example of data that we send to update: 

    {
        "id": int,
        "source_to_img" : str (path in static images),
        "name" : str,
        "price" : float | int,
        "description" : str,
        "featured_products" : bool
    }

## DELETE request

You can delete media from page / (Postman recommended)

* Go to Postman
* Query example: _http://HOST:5000/index/delete_

        {
            "id": int
        }


# .env
## Below should be your data to project
    HOST - mongodb host
    PORT - mongodb port
    DBNAME - mongodb dbname 
    MAIN_COL - mongodb collection name
    TOKEN - token to do REST API (should be - MAX2288)

### Real data, that you can send
After start project you can open another terminal and run init.py,
it should fill the database

# NOTICE
If you wont to do POST, PUT, DELETE requests you should add header that called Authorization





