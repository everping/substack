from bs4 import BeautifulSoup
from substack.plugins.search_plugin import SearchPlugin

class CrtsearchPlugin(SearchPlugin):
    def __init__(self):
        SearchPlugin.__init__(self)
        self.base_url = "https://crt.sh/?q=%25.{query}"

    def get_query(self):
        return self.base_domain.domain_name

    def get_total_page(self):
        return 1

    def get_page_no(self, seed):
        return None

    def extract(self, url):
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}
        content = self.requester.get(url,headers=headers).text
        soup = BeautifulSoup(content, "html5lib")
        search = soup.find_all("td", attrs={"class":"outer"})
        for i in search[1].find_all("td", attrs={"style":None,"href":None}):
            if not i.findChildren():
                try:
                    self.add(i.string)
                except:
                    pass