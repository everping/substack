import json


class Config(dict):
    def __init__(self):
        dict.__init__(self)
        self._default()

    def save(self, variable_name, value):
        """
        This method saves the variable_name value to a dict.
        """
        self[variable_name] = value

    def load(self, variable_name):
        """
        Returns the data that was saved to the variable_name
        """

        return self.get(variable_name, None)

    def _default(self):
        """
        Set default config
        """
        mode = {
            "discovery": {
                "active": True,
                "engines": [
                    "Bing",
                    "Baidu"
                ]
            },
            "brute_force": {
                "active": False
            }
        }
        request = {
            "agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "proxy": ""
        }
        timeout = 300
        logger = {
            "path": "D:/Everping/Work/Projects/substack/log/substack.log",
            "active": True
        }
        self.save('target', "")
        self.save('mode', mode)
        self.save('timeout', timeout)
        self.save('request', request)
        self.save("logger", logger)

    def load_config(self, config_file):
        configs = json.load(open(config_file, "r"))
        for c in configs:
            self.save(c, configs[c])


config = Config()
