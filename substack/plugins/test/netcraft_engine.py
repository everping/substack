from bs4 import  BeautifulSoup
import requests
from urlparse import urlparse
import time

target = "yahoo.com"
url = "http://searchdns.netcraft.com/?restriction=site+ends+with&host=" + target
r = requests.get(url)

_soup = BeautifulSoup(r.text, "html5lib")
last = ""
_from = ""
total = int(_soup.find_all("em")[0].string.split()[1])
print total
if total > 20:
	count = total / 20
	for tem in range(count+1):
		r = requests.get(url + last + _from)
		soup = BeautifulSoup(r.text, "html5lib")
		search_region = BeautifulSoup(str(soup.find_all("table", attrs={"class":"TBtable"})))
		for item in search_region.find_all('a', attrs={"rel":True}):
			url_temp = urlparse(item['href']).netloc
			print url_temp
		last = "&last="+url_temp
		_from = "&from="+str((tem+1)*20 +1)
		time.sleep(1)
else:
	search_region = BeautifulSoup(str(_soup.find_all("table", attrs={"class":"TBtable"})))
	for item in search_region.find_all('a', attrs={"rel":True}):
		url_temp = urlparse(item['href']).netloc
		print url_temp


