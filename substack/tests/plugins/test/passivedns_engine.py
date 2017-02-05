from bs4 import BeautifulSoup
import requests

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}
target = "google.com"
url = "http://ptrarchive.com/tools/search.htm?label=%s" % target

r = requests.get(url, headers=headers)

soup = BeautifulSoup(r.text, "html5lib")

for item in soup.find_all("tr"):
	temp= item.contents[2].string.split()[0]
	print temp