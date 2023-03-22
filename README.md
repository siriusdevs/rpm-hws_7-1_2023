# .env:

database name, host, port, passsword and user to connect 

- PG_HOST: postgresql host
- PG_USER: postgresql username
- PG_PASSWORD: postgresql password
- PG_PORT: postgresql port
- PG_DBNAME: postgresql dbname

# docker for postgresql and installation of some modules:

- chmod +x requirements/init_script.sh
- ./init_script.sh

# run:
- python3 main.py
