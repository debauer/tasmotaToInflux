from tasmota import Tasmota


class Blitzwolf(Tasmota):
    def __init__(self, message):
        Tasmota.__init__(self, message)

    def get_influx_json(self):
        jsondata = [{
            "measurement": self.measurement,
            "tags": {
                "name": self.name
            },
            "fields": self.payload["ENERGY"]
        }]
        return jsondata
