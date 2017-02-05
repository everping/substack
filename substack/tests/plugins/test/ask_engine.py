import requests
from bs4 import BeautifulSoup
from urlparse import urlparse
max_page = 50
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}

while True:
	url = "http://www.search.ask.com/web?q=site:bkav.com&page=%d" % (max_page)
	r = requests.get(url, headers=header)
	
	if "did not match with any results" not in r.text or "Try fewer keywords" not in r.text:
		soup = BeautifulSoup(r.text)
		search_tags = soup.find_all("cite", attrs={"class":"algo-display-url"})
		for tag in search_tags:
			print urlparse(tag.string).netloc


		search_pages = soup.find_all("a", attrs={"ul-attr-accn":"pagination"})
		list_no_page = []
		for tag in search_pages:
			try:
				no_page = int(tag.string)
				list_no_page.append(no_page)
			except:
				continue
		print max(list_no_page)
		break
	else:
		print url
		max_page = max_page - 5

