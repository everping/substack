import ast
import os
from substack.data.utils import get_plugin_dir

from substack.plugins.search.bing_engine import BingEngine
from substack.plugins.search.baidu_engine import BaiduEngine


class EngineFactory():
    def __init__(self):
        self.plugin_name = ""
        self.plugin_type = ""
        self.requester = None

    def is_valid_plugin_file(self, plugin_file):
        try:
            if not plugin_file.endswith("_engine.py"):
                return False
            if not self.get_class(plugin_file).endswith("Engine"):
                return False
        except:
            return False

        return True

    def get_plugins(self):

        plugins = []

        for dirname, dirnames, filenames in os.walk(os.path.join(get_plugin_dir(), self.plugin_type)):
            for filename in filenames:
                plugin_file = os.path.join(dirname, filename)
                if self.is_valid_plugin_file(plugin_file):
                    plugins.append(self.get_class(plugin_file))

        return plugins

    @staticmethod
    def get_class(plugin_file):
        source = open(plugin_file).read()
        p = ast.parse(source)
        classes = [node.name for node in ast.walk(p) if isinstance(node, ast.ClassDef)]
        return classes[0]

    def create(self):
        if self.plugin_name in self.get_plugins():
            module = __import__(self.plugin_name)
            class_ = getattr(module, class_name)
            instance = class_()

a = EngineFactory()

print a.get_plugins("search")
