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
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            print url
            content = self.requester.get(url).text  # get all text of this page
            soup = BeautifulSoup(content, "lxml")
            tag_a = soup.findAll('a', attrs={'class': 'fl'})
            print tag_a
            num_page = tag_a[-1]['aria-label']
            return int(num_page.split()[1])
        except:
            print "somthing was wrong"
            return 0

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "lxml")
        domains = soup.find_all("cite")

        for line in domains:
            try:
                url = str(line.string.split()[0])

                if url.startswith("https", 0, 5):
                    self.add(urlparse(url).netloc)
                else:
                    url = "http://" + url
                    self.add(urlparse(url).netloc)
            except:
                print "somthing was wrong"
                pass
