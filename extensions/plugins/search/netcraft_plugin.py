from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin
from substack.data.logger import logger


class NetcraftPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "http://searchdns.netcraft.com/?restriction=site+ends+with&host={query}"

    def get_query(self):
        return self.base_domain.domain_name

    def get_page_no(self, seed):
        return ""

    def get_total_page(self):
        return 1

    def has_error(self, response):
        sigs_list = ['Lookup another URL']
        for sig in sigs_list:
            if sig in response:
                return True
        return False

    def extract(self, url):
        try:
            content = self.requester.get(url).text
            if self.has_error(content):
                logger.error("Can not find any result for: %s" % self.base_domain.domain_name)
                return None

            _soup = BeautifulSoup(content, "html5lib")

            if not _soup.find_all("em"):
                logger.error("This site seem to blocked your requests")
                return

            _last = ""
            _from = ""

            total = int(_soup.find_all("em")[0].string.split()[1])
            logger.info("Total of results: %d for: %s " % (total, self.base_domain.domain_name))

            if total > 20:
                count = total / 20
                for tem in range(count + 1):
                    url_temp = ""
                    r = self.requester.get(url + _last + _from)
                    soup = BeautifulSoup(r.text, "html5lib")
                    search_region = BeautifulSoup(str(soup.find_all("table", attrs={"class": "TBtable"})), "lxml")

                    for item in search_region.find_all('a', attrs={"rel": True}):
                        url_temp = self.parse_domain_name(item['href'])
                        self.add(url_temp)
                    _last = "&last=" + url_temp
                    _from = "&from=" + str((tem + 1) * 20 + 1)
            else:
                search_region = BeautifulSoup(str(_soup.find_all("table", attrs={"class": "TBtable"})), "lxml")
                for item in search_region.find_all('a', attrs={"rel": True}):
                    url_temp = self.parse_domain_name(item['href'])
                    self.add(url_temp)
        except:
            raise
