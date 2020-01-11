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
    data = message.topic.split("/")
    device = data[3]
    topic = data[4]
    prefix = data[2]
    devicegroup = data[1]
    roomgroup = data[0]
    if topic == 'LWT':
        pass
    elif topic == 'SENSOR':
        jd = json.loads(message.payload)
        #print(flatten(jd))
        #if "ENERGY" in jd:
        #    print(jd["ENERGY"])
    elif topic == 'STATE':
        pass
    else:
        pass
        #print("%s %s %s %s %s" % (roomgroup, devicegroup, prefix, device, topic))
        #print(message.payload)


def on_ds18b20(mosq, obj, message):
    topic_split = message.topic.split("/")
    topic = topic_split[0]+'_'+topic_split[1]+'_'+topic_split[3]
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
                print(jsondata)
                influxc.write_points(jsondata)

def on_generic(mosq, obj, message):
    print(message.topic)
    pass



mqttc.message_callback_add("ug/temperaturen/+/+/#", on_ds18b20)
mqttc.message_callback_add("ew/steckdosen/+/+/#", on_blitzwolf)
mqttc.on_message = on_generic
mqttc.connect(config.mqtt.broker.ip, config.mqtt.broker.port, 60)
mqttc.subscribe("#", 0)
mqttc.loop_forever()
