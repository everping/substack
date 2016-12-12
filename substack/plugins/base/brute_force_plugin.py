import threading

from substack.data.logger import logger
from substack.data.domain import Domain
from substack.plugins.base.plugin import Plugin


class BruteForcePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.sub_domains = []

    def add(self, **kwargs):
        pass

    def get_type(self):
        return "brute_force"
