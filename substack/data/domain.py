import socket


class Domain:
    """
    This class represents a domain
    """

    def __init__(self, domain_name):
        self.domain_name = domain_name
        self.ip = self._get_ip()
        self.meta_data = {}

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
