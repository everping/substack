import nmap
from substack.plugins.base.port_plugin import PortPlugin


class NmapPlugin(PortPlugin):
    def __init__(self):
        PortPlugin.__init__(self)

    def real_scan(self, domain):
        open_ports = []

        nm = nmap.PortScanner()
        nm.scan(domain.ip)
        host = nm.all_hosts()[0]
        protocols = nm[host].all_protocols()
        for protocol in protocols:
            ports = nm[host][protocol].keys()
            for port in ports:
                open_ports.append(port)

        return open_ports
