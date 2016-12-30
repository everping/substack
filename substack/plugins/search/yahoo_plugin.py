from bs4 import BeautifulSoup
from substack.plugins.base.search_plugin import SearchPlugin
from substack.data.logger import logger

class YahooPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "https://search.yahoo.com/search?p={query}&b={page}"
        self.max_page = 300

    def get_query(self):
        return "site:%s" % self.base_domain.domain_name

    def get_page_no(self, seed):
        return seed * 10

    def get_total_page(self):
        max_page_temp = self.max_page

        while (max_page_temp >= 0):
            url = self.base_url.format(query=self.get_query(), page=max_page_temp)
            content = self.requester.get(url).text
            if self.has_error(content):
                print "To much requests and Yahoo knew"
                return 0
            if (("We did not find results for" not in content) or (
                        "Check spelling or type a new query" not in content)):
                list_seed = []
                soup = BeautifulSoup(content, "html5lib")
                search_page = soup.find_all("a", href=True, title=True, attrs={'class': None})
                for i in search_page:
                    list_seed.append(int(i.string))
                current = soup.find("strong")
                try:
                    list_seed.append(int(current.string))
                except:
                    print "Failed to get current seed but that means there are no more subdomain for this base_domain"
                if not list_seed:
                    return 0
                else:
                    return max(list_seed)
            else:
                max_page_temp -= 50
                print "max_page down to %d since bot can not get any infor about total_page" % (max_page_temp)

    def has_error(self, content):
        list_sig = ["Yahoo! - 999 Unable to process request at this time -- error 999",
                    "This problem may be due to unusual network activity"]
        for temp in list_sig:
            if temp in content:
                return True
        return False

    def extract(self, url):
        content = self.requester.get(url).text
        soup = BeautifulSoup(content, "html5lib")
        search = soup.find_all("a", attrs={"class": " ac-algo ac-21th lh-24"})

        for line in search:
            try:
                url = line['href'].split("/")[7].split("=")[1]
                self.add(self.parse_domain_name(url))
            except:
                logger.error("can not extract domain")
