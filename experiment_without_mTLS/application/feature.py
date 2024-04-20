from pylsl import StreamInlet, resolve_stream
from application.logging import logger
from application.metrics import InfluxDB
import paho.mqtt.client as mqtt
from contextlib import suppress
import json


def on_publish(client, userdata, mid, reason_code, properties):
    with suppress(KeyError):
        userdata.remove(mid)

    logger.info("Message sent successfully.")


def lsl_signal_acquisition():
    logger.info("Starting LSL signal acquisition...")
    streams = resolve_stream()
    inlet = StreamInlet(streams[0])

    while True:
        sample, _ = inlet.pull_sample()
        message = json.dumps({"sample": sample})
        client.publish("mTLS/start", message)


def main(client):
    lsl_signal_acquisition(client)


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_publish = on_publish
    client.connect("10.1.0.44", 1883)

    main(client)
