from flatten_json import flatten

teleSensor = {"Time": "2019-12-19T15:32:04",
              "ENERGY": [{"asd": 1}, {"asd": 2}]}


def Core():
    print(flatten(teleSensor))
