from datetime import datetime
from flatten_json import flatten
import json


class Tasmota:
    def __init__(self, message):
        self.payload = json.loads(message.payload)
        if 'Time' not in self.payload:
            self.time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")  # "2020-01-13T13:29:52"
        self.time = self.payload['Time']
        self.payload.pop('Time', None)  # we remove the time so the flattend json only contains "cool" data
        topic_split = message.topic.split("/")
        self.location = topic_split[0]  # in my case the location in the house like "ew" (einliegerwohnung)
        self.groupname = topic_split[1]  # in my case: Temperatur, Steckdosen
        self.prefix = topic_split[2]  # stat, cmnd, tele
        self.name = topic_split[3]  # in my case the devicename, in tasmota config "topic"
        self.command = topic_split[4]  # see command list: https://github.com/arendst/Tasmota/wiki/Commands
        self.measurement = topic_split[0] + '_' + topic_split[1] + '_' + topic_split[3]  # measurement name for influx ("ew_steckdosen_kuehlschrank"
        self.message = message

    def get_payload(self):
        return self.payload

    def get_flatten_payload(self):
        return flatten(self.payload)

    def get_influx_json(self):
        jsondata = [{
            "measurement": self.measurement,
            "tags": {
                "name": self.name
            },
            "fields": self.get_flatten_payload()
        }]
        return jsondata
