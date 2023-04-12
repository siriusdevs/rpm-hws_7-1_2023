#!/bin/bash

echo "Starting the server"

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

check_code $OK