#!/bin/bash
PG_HOST=127.0.0.1
PG_PORT=5555
PG_USER=test
PG_PASSWORD=test
PG_DBNAME=test
DOCKER_NAME=test
DDL_NAME=db_init.ddl

# set env variables
echo "PG_HOST=$PG_HOST" > .env
echo "PG_PORT=$PG_PORT" >> .env
echo "PG_USER=$PG_USER" >> .env
echo "PG_PASSWORD=$PG_PASSWORD" >> .env
echo "PG_DBNAME=$PG_DBNAME" >> .env
sudo cp first/templates /
# set up database
python3.10 first/setup_db.py

# server start
echo "Starting the server"
python3.10 first/main.py &

# real tests
sleep 2

OK=200
CREATED=201

token=a1b2c3d4-a1b2-c3d4-e5f6-a1b2c3a1b2c3

echo "simple_GET request:"
get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001/`
if [[ $get_code -eq $OK ]]
then
echo "OK"
else
echo "FAILED"
echo "GET_CODE $get_code"
exit 1
fi

echo "POST request:"
post_code=`curl -s -o /dev/null \
    -X POST \
    -d '{"fname": "a1b2c3d4", "lname":"abcdef", "group_":"1"}' \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8001/`
if [[ $post_code -eq $CREATED ]]
then
echo "OK"
else
echo "FAILED"
echo "POST_CODE $post_code"
exit 1
fi

echo "query_GET request:"
get_code=`curl -s -o /dev/null \
    -X GET \
    -w %{http_code} \
    http://127.0.0.1:8001?fname=a1ba1b2c3d42c3d4`
if [[ $get_code -eq $OK ]]
then
echo "OK"
else
echo "FAILED"
echo "GET_CODE $get_code"
exit 1
fi

echo "DELETE request:"
post_code=`curl -s -o /dev/null \
    -X DELETE \
    -H "Authorization:admin {$token}"\
    -w %{http_code} \
    http://127.0.0.1:8001?fname=a1b2c3d4`
if [[ $post_code -eq $OK ]]
then
echo "OK"
else
echo "FAILED"
echo "DELETE_CODE $delete_code"
exit 1
fi

# # clean up
rm .env