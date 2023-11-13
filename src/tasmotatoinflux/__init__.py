import sys
import os

from python_json_config import ConfigBuilder
from influxdb import InfluxDBClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
builder = ConfigBuilder()
configFull = builder.parse_config('config.json')
config = configFull.develop
if configFull.environment == 'production':
    config = configFull.production
broker = config.mqtt.broker
influx = config.influx.database
InfluxClient = InfluxDBClient(influx.ip, influx.port, influx.user, influx.passwort, influx.db)

from .core import Core
