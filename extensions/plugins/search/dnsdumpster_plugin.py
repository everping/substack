from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin
from substack.data.logger import logger


class DnsDumpsterPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "https://dnsdumpster.com/"

    def get_query(self):
        return ""

    def get_page_no(self, seed):
        return ""

    def get_total_page(self):
        return 1

    def has_error(self, response):
        pass

    def extract(self, url):

        site = self.base_domain.domain_name

        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
                  "Cookie": "csrftoken=xW6DIMrTX9qge6cQuCE1OmZgmGunVinw",
                  "Referer": "https://dnsdumpster.com/"}
        payload = {"csrfmiddlewaretoken": "xW6DIMrTX9qge6cQuCE1OmZgmGunVinw",
                   "targetip": site}

        content = self.requester.post(url, payload, header).text
        soup = BeautifulSoup(content, "lxml")
        search_tags = soup.find_all('td', attrs={"class": "col-md-4"})
        if not search_tags:
            logger.info("Plug-in DNsDumpster: can't get any result for: %s" % self.base_domain.domain_name)
            return
        for tag in search_tags:
            domain = tag.contents[0].strip('.')
            if site in domain:
                self.add(domain)
