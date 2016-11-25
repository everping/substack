import requests
from urlparse import urlparse
from bs4 import BeautifulSoup
from engine import Engine


class BingEngine(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.base_url = 'https://www.bing.com/search?q={query}&first={page}'
        self.max_page = 999999

    def get_query(self):
        return "domain:%s" % self.base_domain

    def get_page_no(self, seed):
        return 1 if seed == 0 else seed * 10 - 2

    def get_total_page(self):
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            r = requests.get(url)
            return int(BeautifulSoup(r.text, "lxml").find('a', class_="sb_pagS").string)
        except AttributeError:
            return 1

    def extract(self, url):
        r = requests.get(url)
        content = r.text
        soup = BeautifulSoup(content, "lxml")
        ul = soup.find_all("li", class_="b_algo")
        for li in ul:
            uri = li.find('a')['href']
            domain_name = urlparse(uri).netloc
            self.add(domain_name)


import time

a = time.time()

_domain = "bkav.com"

b = BingEngine()
while 1:
    subs = b.discover(_domain)
    print '.'

    if subs.__len__() != 7:
        for d in subs:
            print d.domain_name
        break

# print b.discover(_domain).__len__()
b = time.time()
print b - a
