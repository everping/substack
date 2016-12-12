import threading
from substack.data.logger import logger
from substack.plugins.base.plugin import Plugin


class PortPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.open_ports = []
        self.lock = threading.Lock()

    def add(self, port):
        """
        Add the sub-domain to the result list
        """
        self.lock.acquire()

        if self.is_existed(port):
            self.lock.release()
            return

        try:
            self.open_ports.append(port)
        finally:
            self.lock.release()

    def is_existed(self, port):
        """
        Check if this port exist in result list
        """
        return port in self.open_ports

    def get_type(self):
        return "port"

    def scan(self, domain):
        open_ports = self.real_scan(domain)
        return open_ports

    def real_scan(self, domain):
        msg = 'Plugin is not implementing required method real_scan'
        raise NotImplementedError(msg)
