import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        if Path(self.config_file).exists():
            with open(self.config_file, 'r') as file:
                return json.load(file)
        return {}

    def get_config(self, key, default=None):
        return self.config_data.get(key, default)

    def set_config(self, key, value):
        self.config_data[key] = value
        with open(self.config_file, 'w') as file:
            json.dump(self.config_data, file, indent=4)
