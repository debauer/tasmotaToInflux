from dataclasses import dataclass, field
from typing import Any

from python_json_config import Config


@dataclass
class Device:
    device_name: str = "undefined"
    alias_name: str = "undefined"
    description: str = "no description found"

    def __str__(self):
        return {
            "device_name": self.device_name,
            "description": self.description,
            "alias_name": self.alias_name,
        }


devices = [
    #1wire without "28-" prefix
    Device("01143F8976AA", "vorlauf_fussbodenheizung", "Vorlauf FBH"),
    Device("01143F625BAA", "ruecklauf_fussbodenheizung", "Ruecklauf FBH"),
    Device("01143F7D25AA", "vorlauf_heizkoerper", "Vorlauf HK"),
    Device("01143D2FD7AA", "ruecklauf_heizkoerper", "Ruecklauf HK"),
    Device("01143D5252AA", "abgas", "Abgas"),
    Device("01143F683AAA", "warmwasser", "Warmwasser"),
    Device("011927CADC65", "teich", "Teich"),
    Device("011927A00E0F", "gartenboden", "Boden"),
    Device("steckdose01", "Technik Lager"),
    Device("steckdose02", "Kühlschrank"),
    Device("steckdose03", "Spüma"),
    Device("steckdose04", "Hundebrunnen"),
    Device("steckdose05", "Nadine"),
    Device("steckdose06", "fernseher"),
    Device("steckdose07", "tbd"),
    Device("steckdose08", "david"),
    Device("steckdose09", "terra"),
    Device("steckdose10", "klima"),
    Device("steckdose11", "Büro"),
]


@dataclass
class ConfigWrapper:
    config: Config
    mqtt: Config = field(init=False)
    influxdb: Config = field(init=False)
    devices: list[Device] = field(init=False)

    def __post_init__(self) -> None:
        self.mqtt = self.config.mqtt
        self.influxdb = self.config.influxdb
        self.devices = devices

    def _find_device(self, device_name: str):
        for d in self.devices:
            if d.device_name.upper() == device_name.upper():
                return d
        return Device(device_name=device_name.lower())

    def device(self, type: str, device_name: str) -> Device:
        if type in ["onewire", "powerplug"]:
            return self._find_device(device_name=device_name)
        raise NotImplementedError()
