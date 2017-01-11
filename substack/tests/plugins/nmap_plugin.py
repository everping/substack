from extensions.plugins.port.nmap_plugin import NmapPlugin
from substack.data.domain import Domain


domain = Domain('bkav.com')
plugin = NmapPlugin()
print plugin.scan(domain)
