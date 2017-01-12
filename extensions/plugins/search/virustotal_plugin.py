from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin
from substack.data.logger import logger


class VirusTotalPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "https://www.virustotal.com/vi/domain/{query}/information/"

    def get_query(self):
        return self.base_domain.domain_name

    def get_page_no(self, seed):
        return ""

    def get_total_page(self):
        return 1

    def has_error(self, response):
        list_sigs = ['VirusTotal is trying to prevent scraping and abuse, we are going to bother']
        for sig in list_sigs:
            if sig in response:
                return True
        return False

    def extract(self, url):
        headers = {
            "Cookie": "VT_PREFERRED_LANGUAGE=en; __utma=194538546.1669411933.1482685628.1482685628.1482685628.1;"
                      " __utmb=194538546.1.10.1482685628; __utmc=194538546;"
                      " __utmz=194538546.1482685628.1.1."
                      "utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided);"
                      " __utmt=1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
            "Host": "www.virustotal.com"
        }
        content = self.requester.get(url,headers).text
        if not self.has_error(content):
            try:
                soup = BeautifulSoup(content, "html5lib")
                search_tags = soup.find_all("a", attrs={"target": "_blank", "class": None}, href=True)
                for tag in search_tags:
                    domain = tag.string
                    if domain is not None:
                        domain = domain.strip()
                        self.add(domain)
                    else:
                        break
            except:
                pass
        else:
            logger.error("Captcha detected during running VirusTotal Plugin")
