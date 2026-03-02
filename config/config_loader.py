import json

class ConfigLoader:
    def __init__(self, path="config/qpu_config.json"):
        with open(path) as f:
            self.cfg = json.load(f)

    def get(self, key):
        return self.cfg.get(key)