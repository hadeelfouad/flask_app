import json
import logging

import paho.mqtt.client as mqtt

from errors import MQTTConnectionError

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
        except ConnectionRefusedError as e:
            logging.error("Failed to connect to server with error: {}".format(repr(e)))
            raise MQTTConnectionError()

    @staticmethod
    def on_message(client, userdata, msg):
        stock = json.loads(msg.payload)
        stocks[stock['stock_id']] = stock


# if __name__ == "__main__":
#     client = VerneConsumer(host="10.118.244.251", topic="thndr-trading")
#     i = 0
#     while True:
#         i += 1
