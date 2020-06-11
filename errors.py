
class MQTTConnectionError(Exception):

    def __init__(self, message="Failed to connect to MQTT server"):
        super().__init__(message)