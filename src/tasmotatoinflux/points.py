from dataclasses import dataclass
from dataclasses import field
from typing import Any

from tasmotatoinflux.config_wrapper.wrapper import ConfigWrapper


@dataclass
class InfluxPoint:
    mqtt_topic: list[str]
    mqtt_payload: dict[str, Any]
    config: ConfigWrapper

    measurement: str = field(init=False)
    datapoints: list[dict[str, any]] = field(init=False)

    _blacklist = ["Time", "Sleepmode", "Sleep", "PressureUnit", "TempUnit"]

    def __str__(self) -> str:
        return f"{'/'.join(self.mqtt_topic)}, {self.measurement=}"

    def __post_init__(self) -> None:
        self.datapoints = []
        self.measurement = f"{self.mqtt_topic[0]}_{self.mqtt_topic[1]}"
        self._datapoints()

    def _add_datapoint(self, config_data, values):
        self.datapoints.append(
            {
                "measurement": self.measurement,
                "tags": {
                    "alias_name": config_data.alias_name,
                    "device_name": config_data.device_name,
                },
                "fields": values,
            }
        )

    def _to_datapoint(self, values):
        config_data = self.config.device("powerplug", self.mqtt_topic[3])
        self._add_datapoint(config_data, values)

    def _to_1wire_datapoint(self, values):
        config_data = self.config.device("onewire", values["Id"])
        values = {"temperature": float(values["Temperature"])}
        self._add_datapoint(config_data, values)

    def _datapoints(self) -> None:
        for key, value in self.mqtt_payload.items():
            if key[:7] == "DS18B20":
                self._to_1wire_datapoint(value)
            elif key not in self._blacklist:
                self._to_datapoint(value)
