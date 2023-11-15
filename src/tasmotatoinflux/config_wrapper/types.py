from dataclasses import dataclass


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


@dataclass
class MqttBroker:
    address: str
    port: int
    auth: bool
    user: str
    password: str


@dataclass
class InfluxDB:
    address: str
    user: str
    password: str
    auth: bool = True
    database_name: str = "tasmota"
    port: int = 8086
    bulk_size: int = 5
