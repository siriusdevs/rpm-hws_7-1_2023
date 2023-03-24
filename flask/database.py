from config import *
import logging
from logger import init_logger


init_logger('database')
logger = logging.getLogger("database")


def get_from_db(client):
    db = client[f'{DBNAME}']
    coll = db.MAIN_COL
    res = coll.find()
    logger.info('Get from database!')
    return res


def fill_db(client, data_to_insert):
    db = client[f'{DBNAME}']
    coll = db.MAIN_COL
    data_to_insert['_id'] = data_to_insert['id']
    del data_to_insert['id']
    coll.insert_one(data_to_insert)
    logger.info('Inserted data succesfully!')
    return data_to_insert


def delete_from_db(client, id_from_user):
    db = client[f'{DBNAME}']
    coll = db.MAIN_COL
    result_to_user = coll.delete_one({"_id": id_from_user['id']})
    logger.info(f"Deleted document with ID {id_from_user}")
    return result_to_user.deleted_count


def update_db(client, id_from_user, new_data):
    db = client[f'{DBNAME}']
    coll = db.MAIN_COL
    result_to_user = coll.update_one({"_id": id_from_user}, {"$set": new_data})
    logger.info(f"Updated document with ID {id_from_user}")
    return result_to_user.modified_count
