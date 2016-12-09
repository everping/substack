from substack.plugins.port.mxtoolbox_plugin import MxToolboxPlugin
from substack.data.domain import Domain
from substack.data.requester import Requester


plugin = MxToolboxPlugin()
domain = Domain('bkav.com')
requester = Requester()

plugin.set_requester(requester)
plugin.scan(domain)