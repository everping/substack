from bs4 import BeautifulSoup
from substack.data.logger import logger
from substack.plugins.base.search_plugin import SearchPlugin

class AskPlugin(SearchPlugin):
	def __init__(self):
		SearchPlugin.__init__(self)
		self.base_url = "http://www.search.ask.com/web?q={query}&page={page}"
		self.max_page = 50
		print "tesssssssssssssssssssss"
		
	def get_query(self):
		return "site:%s" % self.base_domain.domain_name

	def get_page_no(self, seed):
		return seed

	def get_total_page(self):
		max_page_temp = self.max_page
		
		while True:
			url = self.base_url.format(query = self.get_query(),page = max_page_temp)
			content = self.requester.get(url).text
			if "did not match with any results" not in content or "Try fewer keywords" not in content:
				soup = BeautifulSoup(content, "html5lib")
				search_pages = soup.find_all("a", attrs={"ul-attr-accn":"pagination"})
				list_no_page = []
				for tag in search_pages:
					try:
						no_page = int(tag.string)
						list_no_page.append(no_page)
					except:
						continue
				return max(list_no_page)
				break
			else:
				max_page_temp = max_page_temp - 5
				logger.error("max_page down to %d" % max_page)

	def has_error(self, response):
        error_messages = ['Your client does not have permission to get URL',
                          'Our systems have detected unusual traffic from your computer network']
        for message in error_messages:
            if message in response:
                return True
        else:
            return False

	def extract(self, url):
		content = self.requester.get(url).text
		soup = BeautifulSoup(content, "html5lib")
		search_tags = soup.find_all("cite", attrs={"class":"algo-display-url"})
		for tag in search_tags:
			self.add(self.parse_domain_name(tag.string))
