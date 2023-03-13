from config import *
import logging
from logger import init_logger


init_logger('main')
logger = logging.getLogger("main")


def fill_database(client, data):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    logger.info('Create database succesfully!')
    data['_id'] = data['id']
    del data['id']
    coll.insert_one(data)
    logger.info('Inserted data succesfully!')


def get_from_db(client):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    res = coll.find()
    logger.info('Get from database!')
    return res


def update_db(client, id, new_data):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    result = coll.update_one({"_id": id}, {"$set": new_data})
    logger.info(f"Updated document with ID {id}")
    return result.modified_count


def delete_from_db(client, id):
    db = client[f'{DBNAME}']
    coll = db.COLNAME
    result = coll.delete_one({"_id": id})
    logger.info(f"Deleted document with ID {id}")
    return result.deleted_count
