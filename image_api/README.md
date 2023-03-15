# Install

- pip install -r requirements.txt

# .env

- NASA_API: default="DEMO_KEY" only 30 requests per hour. You can register you api on https://api.nasa.gov/
- PG_HOST: postgresql host
- PG_USER: postgresql username
- PG_PASSWORD: postgresql password
- PG_PORT: postgresql port
- PG_DBNAME: postgresql dbname

# First run 

- python init.py
- Enter your admin username

# Run 
- uvicorn src.main:app --reload
- Go to http://127.0.0.1:8000/
