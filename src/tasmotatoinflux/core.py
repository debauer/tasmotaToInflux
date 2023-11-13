from influxdb import InfluxDBClient
from python_json_config import ConfigBuilder
import json
import paho.mqtt.client as mqtt

from tasmotatoinflux.config import ConfigWrapper
from tasmotatoinflux.points import InfluxPoint


def main() -> None:
    def on_message(mosq, obj, message) -> None:
        topic_split = message.topic.split("/")
        if topic_split[4] == "SENSOR":
            jd: dict = json.loads(message.payload)
            if isinstance(jd, dict):
                points = InfluxPoint(topic_split, jd, config)
                try:
                    influxc.write_points(points.datapoints)
                except Exception as e:
                    print(f"error on name: {topic_split[3]} topic: {message.topic}")
                    print(f"{e}")

    def on_generic(mosq, obj, message) -> None:
        pass
        # print("generic:" + message.topic)

    builder = ConfigBuilder()
    config = builder.parse_config("config.json")

    config = ConfigWrapper(config)

    influxc = InfluxDBClient(
        config.influxdb.database.ip,
        config.influxdb.database.port,
        config.influxdb.database.user,
        config.influxdb.database.password,
        config.influxdb.database.name,
    )
    mqttc = mqtt.Client()
    mqttc.message_callback_add("+/+/tele/+/#", on_message)
    mqttc.on_message = on_generic
    mqttc.connect(config.mqtt.broker.ip, config.mqtt.broker.port, 60)
    mqttc.subscribe("#", 0)
    mqttc.loop_forever()


if __name__ == "__main__":
    main()
