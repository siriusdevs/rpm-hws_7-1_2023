"""Configuration file."""
# HTTP server error codes
NOT_FOUND = 404
FORBIDDEN = 403
BAD_REQUEST = 400
BAD_REQUEST = 400
NOT_IMPLEMENTED = 501

# HTTP OK codes
OK = 200
CREATED = 201
NO_CONTENT = 204

# Paths
PERSON_PATH = "/gen_person"
COMPANY_PATH = "/gen_company"
CLEAR_TABLE_PATH = "/clear_table"

# Database requests
TABLE = "people"
SELECTOR = "SELECT * FROM people"
INSERT = "INSERT INTO {table} ({keys}) VALUES ({values})"
GET_TOKEN = "SELECT token FROM token WHERE username='{username}'"
UPDATE = "UPDATE {table} SET {request}"
DELETE = "DELETE FROM {table} "
FIRST_LINE = "SELECT * FROM {table} LIMIT 1"


# Request ATTRS
MAIN_ATTRS = ["id", "fname", "lname", "email"]
DELETE_ATTRS = ["fname", "lname", "email"]
MAIN_REQUIRED_ATTRS = ["fname", "lname", "email"]

# Templates
MAIN_PAGE = "templates/index.html"
ERROR_PAGE = "templates/error.html"
COMPANY_TEMPLATE = "templates/generate_company.html"
PERSON_TEMPLATE = "templates/generate_person.html"
CLEAR_TABLE = "templates/clear_table.html"

# Host and port
HOST = "127.0.0.1"
PORT = 8001

# Html headers
CONTENT_LENGTH = "Content-Length"
CONTENT_TYPE = "Content-Type", "text/html"
AUTH = "Authorization"

# Coding
CODING = "utf-8"

# API URLs
PERSON_URL = "https://fakerapi.it/api/v1/persons?_quantity=1"
COMPANY_URL = "https://fakerapi.it/api/v1/companies?_quantity=1"

# API bad response
API_KEY_ERROR = {"Bad request": "Authorization error with token or username"}
