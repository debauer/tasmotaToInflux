from dataclasses import dataclass, field
from python_json_config import Config
from tasmotatoinflux.config_wrapper.types import Device, InfluxDB, MqttBroker
from tasmotatoinflux.config import DEVICES, INFLUX_DB, MQTT_BROKER


@dataclass
class ConfigWrapper:
    mqtt: MqttBroker
    influxdb: InfluxDB
    devices: list[Device]

    def _find_device(self, device_name: str):
        for d in self.devices:
            if d.device_name.upper() == device_name.upper():
                return d
        return Device(
            device_name=device_name.lower(),
            alias_name=device_name.lower(),
            description="device not found in config"
        )

    def device(self, type: str, device_name: str) -> Device:
        if type in ["onewire", "powerplug"]:
            return self._find_device(device_name=device_name)
        raise NotImplementedError()
