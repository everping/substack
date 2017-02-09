from substack.data.domain import Domain
from substack.data.requester import Requester
from substack.plugins.search.google_plugin import GooglePlugin

plugin = GooglePlugin()
domain = Domain('bkav.com')

requester = Requester()
requester.set_agent("Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0")

plugin.set_requester(requester)

plugin.base_domain = domain

print plugin.get_total_page("https://www.google.com/search?q=site:btm.bkav.com&start=500")
