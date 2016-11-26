import socket
import re


class Domain:
    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.ip = self._get_ip()
        self.meta_data = {}

    def _get_ip(self):
        try:
            return socket.gethostbyname(self.domain_name)
        except socket.gaierror:
            return None

    def is_live(self):
        return self.ip is not None

    def save_info(self, variable_name, value):
        self.meta_data[variable_name] = value
