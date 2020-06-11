import logging
import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from consumers import VerneConsumer
from controllers import controller
from database_config import Base, engine

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.ERROR)

app = Flask(__name__)
app.register_blueprint(controller)
try:
    Base.metadata.create_all(engine)
    if bool(os.environ.get("POPULATE_DB", "True")):
        from populator import populate
        populate()
except Exception:
    logging.error("Error while conecting/populating DB")
    raise 

@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code
       
# api = Api(app)
# api.add_resource(HelloWorld, '/hello')

if __name__ == '__main__':
    VerneConsumer(host="10.118.244.251", topic="thndr-trading")
    app.run(debug=bool(os.environ.get("DEBUG_MODE", False)))
