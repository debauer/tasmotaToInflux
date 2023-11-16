from __future__ import annotations

from tasmotatoinflux.config_wrapper.types import Device
from tasmotatoinflux.config_wrapper.types import InfluxDB
from tasmotatoinflux.config_wrapper.types import MqttBroker


DEVICES = [
    # 1wire without "28-" prefix
    Device("01143F8976AA", "vorlauf_fussbodenheizung", "Vorlauf FBH"),
    Device("01143F625BAA", "ruecklauf_fussbodenheizung", "Ruecklauf FBH"),
    Device("steckdose01", "Technik Lager"),
    Device("steckdose02", "Kühlschrank"),
]
dummy_pw = "eva"
MQTT_BROKER = MqttBroker(
    address="herbert",
    port=1883,
    auth=False,
    user="adam",
    password=dummy_pw,
)

INFLUX_DB = InfluxDB(
    address="herbert",
    user="tasmota",
    auth=True,
    port=8086,
    password="asdf",  # noqa: S106
    database_name="tasmota",
    bulk_size=5,
)
