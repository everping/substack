from urlparse import urlparse
from bs4 import BeautifulSoup
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
        try:
            url = self.base_url.format(query=self.get_query(), page=self.max_page)
            content = self.requester.get(url).text
            if (self.captcha_handle(content)):
                soup = BeautifulSoup(content, "html5lib")
                tag_a = soup.findAll('a', attrs={'class': 'fl'})
                num_page = tag_a[-1]['aria-label']
                return int(num_page.split()[1])
            else:
                print "captcha detected [google]"
                return 0
        except:
            print "somthing was wrong in get_total_page"
            return 0

    def captcha_handle(self, text):
        if ("Our systems have detected unusual traffic from your computer network" not in text):
            return True
        else:
            return False

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        search_region = soup.findAll("div", attrs={"id":"search"})
        search_region = BeautifulSoup(str(search_region), "html5lib")
        search_cite = search_region.find_all("cite")

        for line in search_cite:
            try:    
                url = str(line.string.split()[0])

                if url.startswith("https", 0, 5):
                    self.add(urlparse(url).netloc)
                else:
                    url = "http://" + url
                    self.add(urlparse(url).netloc)
            except: 
                print "somthing was wrong in extracting domains"
                pass