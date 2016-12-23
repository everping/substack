from bs4 import BeautifulSoup
from substack.data.logger import logger
from substack.plugins.base.search_plugin import SearchPlugin


class AskPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "http://www.search.ask.com/web?q={query}&page={page}"
        self.max_page = 50

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return seed

    def get_total_page(self):
        max_page_temp = self.max_page

        while True:
            url = self.base_url.format(query=self.get_query(), page=max_page_temp)
            content = self.requester.get(url).text
            if "did not match with any results" not in content or "Try fewer keywords" not in content:
                soup = BeautifulSoup(content, "html5lib")
                search_pages = soup.find_all("a", attrs={"ul-attr-accn": "pagination"})
                list_no_page = []
                for tag in search_pages:
                    try:
                        no_page = int(tag.string)
                        list_no_page.append(no_page)
                    except:
                        continue
                return max(list_no_page)
            else:
                max_page_temp -= 5
                logger.info("max_page down to %d" % max_page_temp)

    def has_error(self, response):
        messages = ['did not match with any results'
                    'Try fewer keywords']
        if messages[0] not  in response or messages[1] not in response:
            return False
        return True

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        search_tags = soup.find_all("cite", attrs={"class": "algo-display-url"})
        for tag in search_tags:
            self.add(self.parse_domain_name(tag.string))
