from urlparse import urlparse
from bs4 import BeautifulSoup
from engine import Engine
from objects.requester import requester


class BingEngine(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.base_url = 'https://www.bing.com/search?q={query}&first={page}'
        self.max_page = 500

    def get_query(self):
        return "domain:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return 1 if seed == 0 else seed * 10 - 2

    def get_total_page(self):
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            content = requester.get_body(url)
            return int(BeautifulSoup(content, "lxml").find('a', class_="sb_pagS").string)
        except AttributeError:
            return 1

    def extract(self, url):
        content = requester.get_body(url)
        soup = BeautifulSoup(content, "lxml")
        ul = soup.find_all("li", class_="b_algo")
        for li in ul:
            uri = li.find('a')['href']
            domain_name = urlparse(uri).netloc
            self.add(domain_name)
