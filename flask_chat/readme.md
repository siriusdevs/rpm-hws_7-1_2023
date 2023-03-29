# Install

- pip install -r requirements.txt

# env

- PG_HOST: postgresql host
- PG_USER: postgresql username
- PG_PASSWORD: postgresql password
- PG_PORT: postgresql port
- PG_DBNAME: postgresql dbname

# First run 

- docker run -d --name chat_project -p 5439:5432 -v $HOME/postgres/chat_project:/var/lib/postgres/chat_project -e POSTGRES_PASSWORD=123456 -e POSTGRES_USER=user -e POSTGRES_DB=chat postgres
- python3 setup_env.py
- python3 filling_db.py
- python3 main.py
- Go to http://127.0.0.1:5000/

# How it should look

![alt text](example/chat.png)

