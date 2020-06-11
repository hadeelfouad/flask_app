import json
import logging

import paho.mqtt.client as mqtt

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)
stocks = {}



class VerneConsumer:
    def __init__(self, topic, host="127.0.0.1", port=1883, keep_alive=10):
        client = mqtt.Client()
        client.on_message = VerneConsumer.on_message
        try:
            client.connect(host, port, keep_alive)
            client.subscribe(topic)
            client.loop_start()
        except Exception as e:
            logging.error("Failed to connect to Mqtt server")
            raise

    @staticmethod
    def on_message(client, userdata, msg):
        stock = json.loads(msg.payload)
        stocks[stock['stock_id']] = stock
