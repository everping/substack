from bs4 import BeautifulSoup
from substack.data.logger import logger
from substack.plugins.base.search_plugin import SearchPlugin


class GooglePlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = 'https://www.google.com/search?q={query}&start={page}'
        self.max_page = 500

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return seed * 10

    def get_total_page(self):
        url = self.base_url.format(query=self.get_query(), page=self.max_page)
        content = self.requester.get(url).text
        if not self.has_error(content):
            soup = BeautifulSoup(content, "html5lib")
            tag_a = soup.findAll('a', attrs={'class': 'fl'})
            try:
                num_page = tag_a[-1]['aria-label']
                return int(num_page.split()[1])
            except:
                logger.error("Can not get total_page so return 0")
                return 0
        else:
            logger.error("Google seems blocked my request")
            return 0

    def has_error(self, response):
        error_messages = ['Your client does not have permission to get URL',
                          'Our systems have detected unusual traffic from your computer network']
        for message in error_messages:
            if message in response:
                return True
        else:
            return False

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        search_region = soup.find_all("div", attrs={"id": "search"})[0]
        search_cite = search_region.find_all("cite")
        for line in search_cite:
            try:
                url = str(line.string.split()[0])
                domain_name = self.parse_domain_name(url)
                self.add(domain_name)
            except:
                pass
