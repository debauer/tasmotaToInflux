from __future__ import annotations

from dataclasses import dataclass

from tasmotatoinflux.config_wrapper.types import Device
from tasmotatoinflux.config_wrapper.types import InfluxDB
from tasmotatoinflux.config_wrapper.types import MqttBroker


@dataclass
class ConfigWrapper:
    mqtt: MqttBroker
    influxdb: InfluxDB
    devices: list[Device]

    def _find_device(self, device_name: str) -> Device:
        for d in self.devices:
            if d.device_name.upper() == device_name.upper():
                return d
        return Device(
            device_name=device_name.lower(),
            alias_name=device_name.lower(),
            description="device not found in config",
        )

    def device(self, device_name: str) -> Device:
        return self._find_device(device_name=device_name)
