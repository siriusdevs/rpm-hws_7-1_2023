from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv
import logging


logger = logging.getLogger("main")
load_dotenv()

DBNAME = getenv('DBNAME')
COLNAME = getenv('COLNAME')
TOKEN = getenv('TOKEN')
HOST = getenv('HOST')
PORT = getenv('PORT')
try:
  APP_PORT = int(getenv('APP_PORT'))
except ValueError:
  logger.info('WRONG PORT!')
else:
  APP_PORT=8000


QUERY = """
  {
    Page {
      media {
        siteUrl
        title {
          english
          native
        }
        description
      }
    }
  }
"""

URL = 'https://graphql.anilist.co'


CLIENT = MongoClient(
    f"mongodb://{HOST}:{PORT}/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.8.0"
)


MESSAGE = "Media {0} successfully"