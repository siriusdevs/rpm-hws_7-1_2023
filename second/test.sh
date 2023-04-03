#!/bin/bash
PG_HOST=127.0.0.1
PG_PORT=5555
PG_USER=test
PG_PASSWORD=test
PG_DBNAME=test
DOCKER_NAME=test
DDL_NAME=init.ddl

# set env variables
echo "PG_HOST=$PG_HOST" > second/.env
echo "PG_PORT=$PG_PORT" >> second/.env
echo "PG_USER=$PG_USER" >> second/.env
echo "PG_PASSWORD=$PG_PASSWORD" >> second/.env
echo "PG_DBNAME=$PG_DBNAME" >> second/.env

# set up database
python3.10 second/setup_db.py

# server start
echo "Starting the chat"
python3 -m flask --app second/app.py run &

# real tests
sleep 2

echo "POST request:"
post_code=`curl -s -o /dev/null \
  -X POST \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=a1b2c3d4&email=abcdef@bb.ru&password=com&copy_password=com" \
  -w %{http_code} \
  http://127.0.0.1:5000/registration`
if [[ $post_code -eq $CREATED ]]
then
echo "OK"
else
echo "FAILED"
echo "POST_CODE $post_code"
exit 1
fi

# clean up
rm second/.env