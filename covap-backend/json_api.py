from flask import Flask
from flask import jsonify
from flask import make_response
from flask import make_response
from flask import request
from flask import abort

import db_collections as COL
import pyArango.connection as CON

import click

_DB = None

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Covap!'

@app.route('/api/get_fields', methods=['GET'])
def get_fields():
    if not request.json:
        abort(400)
    
    ret = {}
    for col_cls in COL.__COLLECTIONS:
        ret[col_cls.__name__] = col_cls._field_types

    return jsonify(ret)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Invalid request'}), 400)

@click.command()
@click.option('--url', help='arangodb url')
@click.option('--username', help='username for the db')
@click.option('--password', help='password for the db')
def set_db(url, username, password):
    global _DB

    conn = CON.Connection(
      arangoURL = url,
      username = username,
      password = password,
      verify = True,
      verbose = False,
      statsdClient = None,
      reportFileName = None,
      loadBalancing = "round-robin",
      use_grequests = False,
      use_jwt_authentication=False,
      use_lock_for_reseting_jwt=True,
      max_retries=5
    )

    _DB = conn["Covap"]


if __name__ == '__main__':
    set_db()
    app.run(debug=True)