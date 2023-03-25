from pymongo import MongoClient
from os import getenv
from dotenv import load_dotenv


load_dotenv()

HOST  = getenv('HOST')
PORT  = getenv('PORT')
DBNAME = getenv('DBNAME')
MAIN_COL = getenv('MAIN_COL')
TOKEN = getenv('TOKEN')

CLIENT = MongoClient(f'mongodb://{HOST}:{PORT}/')

OK = 200

CREATED = 201

SUCCEEDED = 204
