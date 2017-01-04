from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin


class PassiveDnsPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = 'http://ptrarchive.com/tools/search.htm?label={query}'

    def get_query(self):
        return self.base_domain.domain_name

    def get_page_no(self, seed):
        return ""

    def get_total_page(self):
        return 1

    def has_error(self, response):
        pass

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        for item in soup.find_all("tr"):
            try:
                temp= item.contents[2].string.split()[0]
                self.add(temp)
            except:
                pass