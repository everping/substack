from urlparse import urlparse
from bs4 import BeautifulSoup
from substack.plugins.base.search_plugin import SearchPlugin
import re


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
        try:
            pattern_3 = "(.*)>([0-9]*)<\/a>"
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            content = self.requester.get(url).text  # get all text of this page
            soup = BeautifulSoup(content, "lxml")
            tag_a = soup.findAll('a', attrs={'class': 'fl'})
            # print tag_a[-1]['aria-label']
            num_page = tag_a[-1]['aria-label']
            return int(num_page.split()[1])

        except AttributeError:
            raise
            # print "Fucking Errors"
            # return 1

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "lxml")
        ul = soup.find_all("cite")
        pattern = "<[^>]*>(.*)<\/[^>]*>"
        pattern_2 = "([^\/]*)\/(.*)"
        for li in ul:
            temp = re.search(pattern, str(li)).group(1)
            if temp[0:5] == "https":
                domain_name = urlparse(temp).netloc
            else:
                domain_name = re.search(pattern_2, str(temp)).group(1)
            self.add(domain_name)
