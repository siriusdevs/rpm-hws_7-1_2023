#!/bin/bash

# set env variables
python3.10 tests/setup_env.py

# set up database
python3.10 tests/setup_db.py

# server start
echo "Starting the server"
python3.10 main.py &

# real tests
sleep 2

OK=200
CREATED=201

token=a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3
function check_code () {
    if [[ $1 -eq $2 ]]
    then
        echo "OK"
    else
        echo "FAILED, CODE: $1"
        exit 1
    fi
}

echo "simple_GET books request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8002/book`

check_code $get_code $OK

echo "simple_GET movie request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8002/movie`

check_code $get_code $OK


echo "POST book request:"

post_code=`curl -s -o /dev/null \
    -X POST \
    -d '{"title": "some book", "volume": 1, "published": 2000}' \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8002/book`

check_code $post_code $CREATED

echo "POST movie request:"

post_code=`curl -s -o /dev/null \
    -X POST \
    -d '{"title": "some movie", "duration": 160, "released": 2000}' \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8002/movie`

check_code $post_code $CREATED


echo "query_GET book request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8002/book?title=some+book`

check_code $get_code $OK

echo "query_GET movie request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8002/movie?title=some+movie`

check_code $get_code $OK


echo "DELETE book request:"

post_code=`curl -s -o /dev/null \
    -X DELETE \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8002/book?title=some+book`

check_code $post_code $OK

echo "DELETE movie request:"

post_code=`curl -s -o /dev/null \
    -X DELETE \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8002/movie?title=some+movie`

check_code $post_code $OK