class KnowledgeBase:
    def __init__(self):
        self._sub_domains = []

    def add_open_ports(self, domain, ports):
        """
        Set open ports for all domain having same IP
        """
        for _domain in self._sub_domains:
            if _domain.ip == domain.ip:
                for port in ports:
                    if port not in _domain.get_open_ports():
                        _domain.add_open_port(port)

    def _is_existed_domain(self, sub_domain):
        """
        Check if this domain exist in result list
        """
        for domain in self._sub_domains:
            if domain.domain_name == sub_domain.domain_name:
                return True
        return False

    def set_sub_domains(self, sub_domains):
        self._sub_domains = sub_domains

    def get_sub_domains(self):
        return self._sub_domains

    def add_sub_domain(self, sub_domain):
        """
        Add the sub-domain to the result list
        If add successfully, return True. Else, return False
        """

        if not self._is_existed_domain(sub_domain):
            self._sub_domains.append(sub_domain)
            return True
        return False
