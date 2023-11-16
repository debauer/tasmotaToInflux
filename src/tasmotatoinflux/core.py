from __future__ import annotations

import json

from argparse import ArgumentParser
from argparse import Namespace
from logging import getLogger
from typing import Any

import paho.mqtt.client as mqtt

from influxdb import InfluxDBClient
from paho.mqtt.client import MQTTMessage

from tasmotatoinflux.config import DEVICES
from tasmotatoinflux.config import INFLUX_DB
from tasmotatoinflux.config import MQTT_BROKER
from tasmotatoinflux.config_wrapper.wrapper import ConfigWrapper
from tasmotatoinflux.points import InfluxPoint


_log = getLogger()


def parse() -> Namespace:
    parser = ArgumentParser(description="System to record the data on a trimodal crane")
    parser.add_argument(
        "-d",
        "--dryrun",
        action="store_const",
        const="dryrun",
        help="don't commit to influxdb",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_const",
        const="verbose",
        help="verbose",
    )
    return parser.parse_args()


def core() -> None:
    def on_message(_mosq: Any, _obj: Any, message: MQTTMessage) -> None:  # noqa: ANN401
        topic_split = message.topic.split("/")
        if topic_split[4] == "SENSOR":
            jd: Any = json.loads(message.payload)
            if isinstance(jd, dict):
                points = InfluxPoint(topic_split, jd, config)
                _log.debug(points)
                if not dryrun:
                    try:
                        influxc.write_points(points.datapoints)
                    except Exception as e:  # noqa: BLE001
                        _log.info(
                            f"error on name: {topic_split[3]} topic: {message.topic}",
                        )
                        _log.debug(f"{e}")

    def on_generic(
        _mosq: Any,  # noqa: ANN401
        _obj: Any,  # noqa: ANN401
        _message: MQTTMessage,
    ) -> None:
        pass
        # print("generic:" + message.topic)

    config = ConfigWrapper(MQTT_BROKER, INFLUX_DB, DEVICES)

    args = parse()
    dryrun = args.dryrun

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
