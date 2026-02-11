import json
import os

class ConfigManager:
    def __init__(self, config_path="config.json"):
        self.config_path = config_path
        self.default_config = {
            "ai": {
                "api_key": "YOUR_API_KEY_HERE",
                "base_url": "https://api.openai.com/v1",
                "model": "gpt-4-turbo"
            },
            "tools": {
                "nuclei_path": "./tools/nuclei",
                "nmap_path": "nmap",
                "oneforall_path": "./tools/OneForAll/oneforall.py",
                "dirsearch_path": "./tools/dirsearch/dirsearch.py"
            }
        }
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as f:
                json.dump(self.default_config, f, indent=4)
            return self.default_config
        
        try:
            with open(self.config_path, "r") as f:
                return json.load(f)
        except Exception:
            return self.default_config

    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def update(self, key, value):
        keys = key.split('.')
        target = self.config
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        target[keys[-1]] = value
        with open(self.config_path, "w") as f:
            json.dump(self.config, f, indent=4)
