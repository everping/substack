from bs4 import BeautifulSoup
from substack.plugins.base.search_plugin import SearchPlugin
from substack.data.logger import logger

class VirustotalPlugin(SearchPlugin):
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
        headers = {"Cookie":"VT_PREFERRED_LANGUAGE=vi; __utma=194538546.702379437.1482145535.1482145535.1482145535.1; __utmb=194538546.7.10.1482145535; __utmc=194538546; __utmz=194538546.1482145535.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}
        content = self.requester.custom_get(url,headers).text
        if not self.has_error(content):
            soup = BeautifulSoup(content)
            search_tags = soup.find_all("a", attrs={"target":"_blank","class":None}, href = True)
            for tag in search_tags:
                domain = tag.string
                if domain is None:
                    continue
                else:
                    self.add(domain)
        else:
            logger.error("Captcha_detected")
