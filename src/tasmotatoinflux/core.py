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

influxc = InfluxDBClient('localhost', 8086, 'root', 'root', 'tasmotaToInflux')
mqttc = mqtt.Client()

blacklist = ["Time", "Sleepmode", "Sleep", "PressureUnit", "TempUnit"]


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


def on_message(mosq, obj, message):
    # print("topic:" + message.topic)
    # print("payload:" + str(message.payload))
    topic_split = message.topic.split("/")
    # print("topic_split:" + str(topic_split))
    try:
        if topic_split[4] == 'SENSOR':
            jd = json.loads(message.payload)
            for key in jd:
                # print("key: " + key)
                if key[:7] == "DS18B20":
                    topic = topic_split[0] + '_' + topic_split[1] + '_' + topic_split[3]
                    config_data = getOneWireConfig(jd[key]['Id'])
                    temperature = float(jd[key]['Temperature'])
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
                elif key not in blacklist:
                    topic = topic_split[0] + '_' + topic_split[1]
                    jsondata = [{
                        "measurement": topic,
                        "tags": {
                            "name": topic_split[3]
                        },
                        "fields": jd[key]
                    }]
                    influxc.write_points(jsondata)
    except:
        print("error on name: " + topic_split[3] + " topic: " + topic)


def on_generic(mosq, obj, message):
    pass
    # print("generic:" + message.topic)


mqttc.message_callback_add("+/+/tele/+/#", on_message)
mqttc.on_message = on_generic
mqttc.connect(config.mqtt.broker.ip, config.mqtt.broker.port, 60)
mqttc.subscribe("#", 0)
mqttc.loop_forever()
