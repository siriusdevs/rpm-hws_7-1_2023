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

function check_code () {
    if [[ $1 -eq $2 ]]
    then
        echo "OK"
    else
        echo "FAILED, CODE: $1"
        exit 1
    fi
}

echo "simple_GET request:"

get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/students`

check_code $get_code $OK