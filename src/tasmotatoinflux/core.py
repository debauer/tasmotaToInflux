from argparse import ArgumentParser

from influxdb import InfluxDBClient
import json
import paho.mqtt.client as mqtt

from tasmotatoinflux.config_wrapper.wrapper import ConfigWrapper
from tasmotatoinflux.config import DEVICES, INFLUX_DB, MQTT_BROKER
from tasmotatoinflux.points import InfluxPoint


def parse():
    parser = ArgumentParser(description="System to record the data on a trimodal crane")
    parser.add_argument("-d", "--dryrun", action="store_const", const="dryrun", help="don't commit to influxdb")
    parser.add_argument("-v", "--verbose", action="store_const", const="verbose", help="verbose")
    return parser.parse_args()


def core() -> None:
    def on_message(mosq, obj, message) -> None:
        topic_split = message.topic.split("/")
        if topic_split[4] == "SENSOR":
            jd: dict = json.loads(message.payload)
            if isinstance(jd, dict):
                points = InfluxPoint(topic_split, jd, config)
                if verbose:
                    print(points)
                if not dryrun:
                    try:
                        influxc.write_points(points.datapoints)
                    except Exception as e:
                        print(f"error on name: {topic_split[3]} topic: {message.topic}")
                        print(f"{e}")

    def on_generic(mosq, obj, message) -> None:
        pass
        # print("generic:" + message.topic)

    config = ConfigWrapper(
        MQTT_BROKER, INFLUX_DB, DEVICES
    )

    args = parse()
    dryrun = args.dryrun
    verbose = args.verbose

    if not dryrun:
        influxc = InfluxDBClient(
            config.influxdb.address,
            config.influxdb.port,
            config.influxdb.user,
            config.influxdb.password,
            config.influxdb.database_name,
        )
    mqttc = mqtt.Client()
    mqttc.message_callback_add("+/+/tele/+/#", on_message)
    mqttc.on_message = on_generic
    mqttc.connect(config.mqtt.address, config.mqtt.port, 60)
    mqttc.subscribe("#", 0)
    mqttc.loop_forever()


if __name__ == "__main__":
    core()
