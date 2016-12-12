from substack.plugins.port.nmap_plugin import NmapPlugin
from substack.data.domain import Domain


domain = Domain('mail49.bkav.com')
plugin = NmapPlugin()
print plugin.scan(domain)
