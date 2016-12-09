from urlparse import urlparse
from bs4 import BeautifulSoup
from substack.plugins.base.search_plugin import SearchPlugin


class GooglePlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = 'https://www.google.com/search?q={query}&start={page}'
        self.max_page = 400

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return seed * 10

    def get_total_page(self):
        url = self.base_url.format(query=self.get_query(), page=self.max_page)
        content = self.requester.get(url).text  # get all text of this page
        soup = BeautifulSoup(content, "html5lib")
        print soup
        print soup.findAll('td', class_="cur")

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "lxml")
        domains = soup.find_all("cite")

        for line in domains:
            url = str(line.string.split()[0])

            if url.startswith("https", 0, 5):
                self.add(urlparse(url).netloc)
            else:
                url = "http://" + url
                self.add(urlparse(url).netloc)