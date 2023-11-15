from tasmotatoinflux.config_wrapper.types import Device, MqttBroker, InfluxDB

DEVICES = [
    # 1wire without "28-" prefix
    Device("01143F8976AA", "vorlauf_fussbodenheizung", "Vorlauf FBH"),
    Device("01143F625BAA", "ruecklauf_fussbodenheizung", "Ruecklauf FBH"),
    Device("steckdose01", "Technik Lager"),
    Device("steckdose02", "Kühlschrank"),
]

MQTT_BROKER = MqttBroker(
    address="herbert",
    port=1883,
    auth=False,
    user="adam",
    password="eva"
)

INFLUX_DB = InfluxDB(
    address="herbert",
    user="tasmota",
    auth=True,
    port=8086,
    password="asdf",
    database_name="tasmota",
    bulk_size=5
)