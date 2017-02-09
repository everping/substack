from bs4 import BeautifulSoup
from substack.data.logger import logger
from substack.plugins.search_plugin import SearchPlugin


class AskPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "http://www.search.ask.com/web?q={query}&page={page}"
        self.max_page = 50
        self.messages = {
            'not_found': ['did not match with any results',
                          'Try fewer keywords'],
            'blocked': ['Your client does not have permission to get the requested']
        }

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return seed

    def get_total_page(self):
        max_page_temp = self.max_page

        while max_page_temp >= 0:
            url = self.base_url.format(query=self.get_query(), page=max_page_temp)
            r = self.requester.get(url)

            if r is None:
                return 0

            content = r.text

            if self.was_blocked(content):
                logger.error("Ask blocked the request")
                return 0

            elif self.was_not_found(content):
                logger.info(
                    "Ask Plug-in: max_page down to %d for domain: %s" % (max_page_temp, self.base_domain.domain_name))
                max_page_temp -= 5

            else:
                soup = BeautifulSoup(content, "html5lib")
                search_pages = soup.find_all("a", attrs={"ul-attr-accn": "pagination"})
                list_no_page = []
                for tag in search_pages:
                    try:
                        no_page = int(tag.string)
                        list_no_page.append(no_page)
                    except:
                        continue
                if not list_no_page:
                    logger.debug(soup)
                    return 1
                else:
                    return max(list_no_page)
        return 0

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        search_tags = soup.find_all("cite", attrs={"class": "algo-display-url"})
        for tag in search_tags:
            self.add(self.parse_domain_name(tag.string))
