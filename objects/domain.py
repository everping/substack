import socket
import re


class Domain:
    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.ip = self._get_ip()
        self.url = self._get_url()

    def _get_ip(self):
        try:
            return socket.gethostbyname(self.domain_name)
        except socket.gaierror:
            return None

    def _get_url(self):
        if not self.domain_name.startswith('http://') or not self.domain_name.startswith('https://'):
            return 'http://' + self.domain_name
        return self.domain_name

    def _is_valid(self):
        domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
        if not domain_check.match(self.domain_name):
            return False
        return True

    def is_live(self):
        return self.ip is not None
