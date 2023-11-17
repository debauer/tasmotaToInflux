from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import ClassVar

from tasmotatoinflux.config_wrapper.types import Device
from tasmotatoinflux.config_wrapper.wrapper import ConfigWrapper


@dataclass
class InfluxPoint:
    mqtt_topic: list[str]
    mqtt_payload: dict[str, Any]
    config: ConfigWrapper

    measurement: str = field(init=False)
    datapoints: list[dict[str, Any]] = field(init=False)

    _blacklist: ClassVar = ["Time", "Sleepmode", "Sleep", "PressureUnit", "TempUnit"]

    def __str__(self) -> str:
        return f"{'/'.join(self.mqtt_topic)}, {self.measurement=}"

    def __post_init__(self) -> None:
        self.datapoints = []
        self.measurement = f"{self.mqtt_topic[0]}_{self.mqtt_topic[1]}"
        self._datapoints()
        
    def _fix_arrays(self, values: dict[str, Any]) -> dict[str, Any]:
        new_dict = {}
        for key, v in values.items():
            if isinstance(v, list):
                for i, element in enumerate(v):
                    new_dict[f"{key}_{i}"] = element
            else:
                new_dict[key] = v
        return new_dict

    def _check_for_arrays(self, values: dict[str, Any]) -> dict[str, Any]:
        for key, v in values.items():
            if isinstance(v, list):
                return self._fix_arrays(values)
        return values

    def _add_datapoint(self, device: Device, values: dict[str, Any]) -> None:
        values = self._check_for_arrays(values)
        self.datapoints.append(
            {
                "measurement": self.measurement,
                "tags": {
                    "alias_name": device.alias_name,
                    "device_name": device.device_name,
                },
                "fields": values,
            },
        )

    def _to_datapoint(self, values: dict[str, Any]) -> None:
        config_data = self.config.device("powerplug", self.mqtt_topic[3])
        self._add_datapoint(config_data, values)

    def _to_1wire_datapoint(self, values: dict[str, Any]) -> None:
        config_data = self.config.device("onewire", values["Id"])
        values = {"temperature": float(values["Temperature"])}
        self._add_datapoint(config_data, values)

    def _datapoints(self) -> None:
        for key, value in self.mqtt_payload.items():
            if key[:7] == "DS18B20":
                self._to_1wire_datapoint(value)
            elif key not in self._blacklist:
                self._to_datapoint(value)
