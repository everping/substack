from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin


class BingPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = 'https://www.bing.com/search?q={query}&first={page}'
        self.max_page = 500

    def get_query(self):
        return "domain:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return 1 if seed == 0 else seed * 10 - 2

    def get_total_page(self):
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            content = self.requester.get(url).text
            return int(BeautifulSoup(content, "lxml").find('a', class_="sb_pagS").string)
        except AttributeError:
            return 1

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "lxml")
        ul = soup.find_all("li", class_="b_algo")
        for li in ul:
            url = li.find('a')['href']
            domain_name = self.parse_domain_name(url)
            self.add(domain_name)
