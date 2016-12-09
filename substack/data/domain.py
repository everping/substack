import socket


class Domain:
    """
    This class represents a domain
    """

    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.ip = self._get_ip()
        self.meta_data = {}
        self.open_ports = []

    def set_open_ports(self, ports):
        self.open_ports = ports

    def get_open_ports(self):
        return self.open_ports

    def get_domain_name(self):
        return self.domain_name

    def _get_ip(self):
        """
        Get the ip of this domain
        """
        try:
            return socket.gethostbyname(self.domain_name)
        except socket.gaierror:
            return None

    def is_live(self):
        """
        A domain is considered to be still alive when it can be resolved to an IP
        """
        return self.ip is not None

    def save_info(self, variable_name, value):
        """
        Add information to meta data field
        """
        self.meta_data[variable_name] = value

    def get_info(self, variable_name):
        """
        Get meta data
        """
        return self.meta_data[variable_name]

