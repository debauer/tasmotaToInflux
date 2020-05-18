from flatten_json import flatten
from influxdb import InfluxDBClient
from python_json_config import ConfigBuilder
import json
import paho.mqtt.client as mqtt

builder = ConfigBuilder()
config = builder.parse_config('config.json')

devices = config.devices
if config.environment == "production":
    config = config.production
else:
    config = config.develop

influxc = InfluxDBClient('herbert', 8086, 'root', 'root', 'tasmotaToInflux')
mqttc = mqtt.Client()

blacklist = ["Time", "Sleepmode", "Sleep"]

def getOneWireConfig(id):
    global devices
    for d in devices.onewire:
        if d['Id'][3:].upper() == id.upper():
            return d
    default = {
        "Name": "undefined",
        "Beschreibung": "no description found",
        "Id": "28-" + id.lower()
    }
    return default


def on_blitzwolf(mosq, obj, message):
    topic_split = message.topic.split("/")
    topic = topic_split[0] + '_' + topic_split[1]
    if topic_split[4] == 'SENSOR':
        jd = json.loads(message.payload)
        if "ENERGY" in jd:
            jsondata = [{
                "measurement": topic,
                "tags": {
                    "name": topic_split[3]
                },
                "fields": jd["ENERGY"]
            }]
            # print(jsondata)
            influxc.write_points(jsondata)


def ds18b20(mosq, obj, message):
    topic_split = message.topic.split("/")
    topic = topic_split[0] + '_' + topic_split[1] + '_' + topic_split[3]
    if topic_split[4] == 'SENSOR':
        jd = json.loads(message.payload)
        for k in jd:
            if k[:7] == "DS18B20":
                config_data = getOneWireConfig(jd[k]['Id'])
                temperature = float(jd[k]['Temperature'])
                jsondata = [{
                    "measurement": topic,
                    "tags": {
                        "name": config_data['Name'],
                        "rom_id": config_data['Id']
                    },
                    "fields": {
                        'Temperature': temperature
                    }
                }]
                influxc.write_points(jsondata)


def on_message(mosq, obj, message):
    topic_split = message.topic.split("/")
    topic = topic_split[0] + '_' + topic_split[1]
    if topic_split[4] == 'SENSOR':
        jd = json.loads(message.payload)
        for key in jd:
            if key in blacklist:
                break
            if key[:7] == "DS18B20":
            jsondata = {
                "measurement": topic,
                "tags": {
                    "name": topic_split[3]
                },
                "fields": jd[key]
            }
            influxc.write_points([jsondata])

mqttc.message_callback_add("ew/steckdosen/+/+/#", on_message)
mqttc.on_message = on_generic
mqttc.connect(config.mqtt.broker.ip, config.mqtt.broker.port, 60)
mqttc.subscribe("#", 0)
mqttc.loop_forever()
