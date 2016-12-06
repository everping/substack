from urlparse import urlparse
from bs4 import BeautifulSoup
from engine import Engine


class BaiduEngine(Engine):
    def __init__(self):
        Engine.__init__(self)
        self.base_url = 'http://www.baidu.com/s?wd={query}&pn={page}'
        self.max_page = 500

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return 10 * seed

    def get_total_page(self):
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            content = self.requester.get_body(url)

            # http://stackoverflow.com/a/25661119/6805843
            soup = BeautifulSoup(content, "html5lib")
            div_page = soup.find('div', id="page")
            return int(div_page.find('strong').find_all('span')[1].string)
        except AttributeError:
            return 1

    def extract(self, url):
        content = self.requester.get_body(url)
        soup = BeautifulSoup(content, "html5lib")
        a_tags = soup.find_all('a', class_="c-showurl")
        for a_tag in a_tags:
            my_url = a_tag.string.strip().replace("...", "")
            if not my_url.startswith("http://") and not my_url.startswith("https://"):
                my_url = "http://" + my_url

            domain_name = urlparse(my_url).netloc
            self.add(domain_name)
