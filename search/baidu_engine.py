import requests
import threading
import time
import random
from urlparse import urlparse
from bs4 import BeautifulSoup
from objects.domain import Domain


class BaiduEngine:
    def __init__(self, domain_name):
        self.sub_domains = []
        self.domain_name = domain_name
        self.base_url = 'http://www.baidu.com/s?wd={query}&pn={page}'
        self.max_page = 500
        self.lock = threading.Lock()

    def is_existed(self, sub_domain_name):
        """
        Check if this domain exist in result list
        """
        if sub_domain_name == self.domain_name:
            return True

        for domain in self.sub_domains:
            if domain.domain_name == sub_domain_name:
                return True

        return False

    def add(self, sub_domain_name):
        """
        Add the sub-domain to the result list
        """
        if self.is_existed(sub_domain_name):
            return

        self.lock.acquire()
        try:
            sub_domain = Domain(sub_domain_name)
            if sub_domain.is_live():
                self.sub_domains.append(sub_domain)
        finally:
            self.lock.release()

    def get_query(self):
        return "site:%s" % self.domain_name

    @staticmethod
    def get_page_no(seed):
        return 10 * seed

    def get_total_page(self):
        url = self.base_url.format(query=self.get_query(), page=self.max_page)
        r = requests.get(url)

        # http://stackoverflow.com/a/25661119/6805843
        soup = BeautifulSoup(r.text, "html5lib")
        div_page = soup.find('div', id="page")
        return int(div_page.find('strong').find_all('span')[1].string)

    def extract(self, url):
        r = requests.get(url)
        content = r.text
        soup = BeautifulSoup(content, "html5lib")
        a_tags = soup.find_all('a', class_="c-showurl")
        for a_tag in a_tags:
            my_url = a_tag.string.strip().replace("...", "")
            if not my_url.startswith("http://") and not my_url.startswith("https://"):
                my_url = "http://" + my_url

            domain_name = urlparse(my_url).netloc
            self.add(domain_name)

    @staticmethod
    def sleep():
        time.sleep(random.randint(2, 5))

    def start(self):
        total_pages = self.get_total_page()

        threads = []
        for i in xrange(total_pages):
            url = self.base_url.format(query=self.get_query(), page=self.get_page_no(i))
            thread = threading.Thread(target=self.extract, args=(url,))

            threads.append(thread)
            thread.start()
            # self.sleep()

        for thread in threads:
            thread.join()

        for domain in self.sub_domains:
            print domain.domain_name, domain.ip

        print self.sub_domains.__len__()


a = time.time()
_domain = "yahoo.com"
d = BaiduEngine(_domain)
d.start()
b = time.time()
print b - a
