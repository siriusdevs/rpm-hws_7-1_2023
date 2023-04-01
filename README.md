# .env:

database name, host, port, passsword and user to connect 

- PG_HOST: postgresql host
- PG_USER: postgresql username
- PG_PASSWORD: postgresql password
- PG_PORT: postgresql port
- PG_DBNAME: postgresql dbname

# docker for postgresql and installation of some modules:

- chmod +x requirements/init_script.sh
- ./requirements/init_script.sh

# run:
- python3 main.py

# POST, PUT, DELETE examples
- You should send requests on http://127.0.0.1:8001/main

POST example: 

- in HEADERS you have "Authorization" as key and "admin {077bc286-8564-4627-84c2-beb7b6af5521}" as value

- in body you have {"phrase":"some_phrase"}: dict with one key = "phrase" and one value = any string


PUT example: 

- in HEADERS you have "Authorization" as key and "admin {077bc286-8564-4627-84c2-beb7b6af5521}" as value 

- in PARAMS you have "number" as key and some int value (number of a phrase on server) as value 

- in body you have {"phrase":"some_phrase"}: dict with one key = "phrase" and one value = any string 


DELETE example: 

- in HEADERS you have "Authorization" as key and "admin {077bc286-8564-4627-84c2-beb7b6af5521}" as value 

- in PARAMS you have "number" as key and some int value (number of a phrase on server) as value 

