import importlib


class PluginFactory():
    def __init__(self, plugin_name, plugin_type, requester):
        self.plugin_name = plugin_name
        self.plugin_type = plugin_type
        self.requester = requester

    def get_plugin_file_name(self):
        return self.plugin_name[:-6].lower() + "_engine"

    def create(self):
        try:
            module = "substack.plugins.%s.%s" % (self.plugin_type, self.get_plugin_file_name())
            plugin_class = getattr(importlib.import_module(module), self.plugin_name)
            instance = plugin_class()
            instance.set_requester(self.requester)
            return instance
        except:
            return None
