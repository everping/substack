import nmap
from substack.plugins.port_plugin import PortPlugin


class NmapPlugin(PortPlugin):
    """
    This class call to nmap library
    """
    def __init__(self):
        PortPlugin.__init__(self)

    def real_scan(self, domain):
        open_ports = []

        nm = nmap.PortScanner()
        results = nm.scan(domain.ip)
        hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
        for host, status in hosts_list:
            if status == "up":
                protocols = nm[host].all_protocols()
                for protocol in protocols:
                    ports = nm[host][protocol]
                    for port in ports:
                        if ports[port]['state'] == 'open':
                            open_ports.append(port)
        return open_ports
