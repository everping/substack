from substack.plugins.search.google_plugin import GooglePlugin
from substack.data.domain import Domain
from substack.data.requester import Requester
plugin = GooglePlugin()
domain = Domain('bkav.com')
requester = Requester()

plugin.set_requester(requester)
plugin.base_domain = domain
plugin.get_total_page()