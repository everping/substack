import json
from substack.data.logger import logger
from substack.plugins.search_plugin import SearchPlugin
from substack.data.exceptions import PluginException


class ThreatCrowdPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={query}"

    def get_query(self):
        return self.base_domain.domain_name

    def get_page_no(self, seed):
        return ""

    def get_total_page(self):
        return 1

    def has_error(self, response):
        pass

    def extract(self, url):
        try:
            content = self.requester.get(url).text
            results = json.loads(content)
            if 'subdomains' in results:
                subs = results['subdomains']
                for sub in subs:
                    self.add(sub)
        except:
            raise PluginException
