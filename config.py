import json


class Config(dict):
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

    def load_file(self):
        configs = json.load(open("D:/Everping/Work/Projects/substack/config.json", "r"))
        for c in configs:
            self.save(c, configs[c])


config = Config()
config.load_file()
