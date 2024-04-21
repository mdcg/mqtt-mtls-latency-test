import json
import threading
import time
from contextlib import suppress
from datetime import datetime

import paho.mqtt.client as mqtt
from application.logging import logger
from application.metrics import InfluxDB
from pylsl import StreamInlet, resolve_stream

UNACKED_PUBLISH = set()
metrics = InfluxDB()


def on_publish(client, userdata, mid, reason_code, properties):
    with suppress(KeyError):
        userdata.remove(mid)


def on_connect(client, userdata, flags, reason_code, properties):
    logger.info(f"Connected with result code: {str(reason_code)}")
    client.subscribe("mTLS/end")


def on_message(client, userdata, msg):
    message = json.loads(msg.payload)
    end_at = datetime.now().isoformat()
    elapsed_time = datetime.fromisoformat(end_at).timestamp() - datetime.fromisoformat(message["start_at"]).timestamp()
    logger.info(elapsed_time)
    metrics.collect(elapsed_time)


def publish_message(client, message):
    msg_info = client.publish("mTLS/start", message, qos=1)
    UNACKED_PUBLISH.add(msg_info.mid)
    while len(UNACKED_PUBLISH):
        time.sleep(0.1)

    msg_info.wait_for_publish()


def lsl_signal_acquisition(client):
    logger.info("Starting LSL signal acquisition...")
    while True:
        try:
            streams = resolve_stream()
            inlet = StreamInlet(streams[0])
        except Exception:
            continue

        break

    while True:
        try:
            sample, timestamp = inlet.pull_sample()
        except Exception:
            logger.exception("No more samples to acquire.")
            break

        start_at = datetime.now().isoformat()
        message = json.dumps({"start_at": start_at})
        publish_message(client, message)


def main(client):
    lsl_signal_acquisition(client)


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.tls_set(ca_certs="ca.crt", certfile="application.crt", keyfile="application.key")
    client.on_publish = on_publish
    client.on_connect = on_connect
    client.on_message = on_message
    client.user_data_set(UNACKED_PUBLISH)
    client.connect("labs.local", 8883)

    threading.Thread(target=client.loop_forever).start()

    main(client)
