from substack.data.logger import logger
from substack.plugins.base.engine import Engine


class PortEngine(Engine):
    def __init__(self):
        Engine.__init__(self)

    def get_type(self):
        return "port"

    def scan(self, domain):
        open_ports = self.real_scan(domain)
        logger.info(
            "%s (%s) open ports: %s" % (domain.domain_name, domain.ip, ", ".join([str(port) for port in open_ports])))
        return open_ports

    def real_scan(self, domain):
        msg = 'Plugin is not implementing required method real_scan'
        raise NotImplementedError(msg)

    def extract(self, response):
        msg = 'Plugin is not implementing required method extract'
        raise NotImplementedError(msg)


