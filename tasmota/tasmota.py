from flatten_json import flatten

class Tasmota:
    def __init__(self, message):
        self.message = message

    def get_message(self):
        return self.message

    def get_flatten_message(self):
        return flatten(self.message)
