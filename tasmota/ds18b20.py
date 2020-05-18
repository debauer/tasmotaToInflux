from tasmota import Tasmota


class Ds18b20(Tasmota):
    def __init__(self, message):
        Tasmota.__init__(self, message)

    def get_influx_json(self):
        config_data = getOneWireConfig(jd[k]['Id'])
        temperature = float(jd[k]['Temperature'])
        jsondata = [{
            "measurement": self.measurement,
            "tags": {
                "name": config_data['Name'],
                "rom_id": config_data['Id']
            },
            "fields": {
                'Temperature': temperature
            }
        }]
        return jsondata
