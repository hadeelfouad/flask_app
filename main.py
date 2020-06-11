import logging
import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from consumers import VerneConsumer
from controllers import controller
from database_config import Base, engine

logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s', level=logging.ERROR)

app = Flask(__name__)
app.register_blueprint(controller)
try:
    Base.metadata.create_all(engine)
except Exception:
    logging.error("Error while conecting to DB")
    raise


app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


if __name__ == '__main__':
    VerneConsumer(
        host=os.environ.get("MQTT_HOST", "127.0.0.1"),
        port=int(os.environ.get("MQTT_PORT", 1883)),
        topic=os.environ.get("MQTT_TOPIC", "thndr-trading")
    )
    app.run(host="0.0.0.0", debug=bool(os.environ.get("DEBUG_MODE", False)))
    if bool(os.environ.get("POPULATE_DB", False)):
        from populator import populate
        populate()
