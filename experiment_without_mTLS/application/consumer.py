import paho.mqtt.client as mqtt
from application.logging import logger


def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Connected with result code: {str(reason_code)}")
    client.subscribe("mTLS/start")


def on_message(client, userdata, msg):
    logger.info(f"{msg.topic}: {str(msg.payload)}")


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("labs.local", 1883)
    client.loop_forever()
