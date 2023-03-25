from flask import Flask, request, render_template
import logging
from config import *
from database import get_from_db, fill_db, delete_from_db, update_db
from flask_pydantic import validate
from checker import AuthTokenRequired
from models import ProductCategoryImage


app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.config['JSON_AS_ASCII'] = False


@app.route("/")
def get_index():
    data_to_user = list(get_from_db(CLIENT))
    return render_template('my_index.html', data=data_to_user)


@app.route("/index/create", methods=['POST'])
@validate(body=ProductCategoryImage)
@AuthTokenRequired
def fill_index():
    try:
        body = request.json
    except Exception as ex:
        logging.error(ex, exc_info=True)
        return '', 400
    temprorary = fill_db(CLIENT, body)
    return 'http://127.0.0.1:5000/#product-{0}'.format(temprorary['_id']), 201


@app.route("/index/delete", methods=['DELETE'])
@AuthTokenRequired
def delete_from_index():
    try:
        deleted_rows = delete_from_db(CLIENT, request.args.get('id'))
    except Exception as ex:
        logging.error(ex, exc_info=True)
        return '', 400
    if deleted_rows == 0:
        return 'Not found data!', 404
    return '', 204


@app.route("/index/update", methods=['PUT'])
@validate(body=ProductCategoryImage)
@AuthTokenRequired
def update_index():
    body = request.json
    try:
        updated_rows = update_db(CLIENT, body['id'], body)
    except Exception as ex:
        logging.error(ex, exc_info=True)
        return '', 400
    if updated_rows == 0:
        return 'You update data already!', 404
    return '', 204


if __name__ == '__main__':
    app.run()
