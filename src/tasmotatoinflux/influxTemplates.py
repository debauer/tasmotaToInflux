teleState = {
    "Time": "2019-12-19T15:32:04",
    "Uptime": "12T02:13:58",
    "UptimeSec": 1044838,
    "Heap": 29,
    "SleepMode": "Dynamic",
    "Sleep": 50,
    "LoadAvg": 19,
    "MqttCount": 4,
    "POWER": "ON",
    "Wifi": {
        "AP": 1,
        "SSId": "bauer_2G",
        "BSSId": "78:8A:20:2A:7E:25",
        "Channel": 11,
        "RSSI": 36,
        "LinkCount": 1,
        "Downtime": "0T00:00:11",
    },
}
teleSensor = {
    "Time": "2019-12-19T15:32:04",
    "ENERGY": {
        "TotalStartTime": "2019-12-06T20:00:40",
        "Total": 14.162,
        "Yesterday": 1.270,
        "Today": 0.004,
        "Period": 0,
        "Power": 0,
        "ApparentPower": 0,
        "ReactivePower": 0,
        "Factor": 0.00,
        "Voltage": 232,
        "Current": 0.000,
    },
}

json_body = [
    {
        "measurement": "onewire",
        "tags": {"name": "vorlauf_fussbodenheizung", "rom_id": "28-01143f625baa"},
        "time": "2009-11-10T23:00:00Z",
        "fields": {
            "Float_value": 0.64,
            "Int_value": 3,
            "String_value": "Text",
            "Bool_value": True,
        },
    }
]
