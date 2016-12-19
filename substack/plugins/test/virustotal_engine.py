import requests
from bs4 import BeautifulSoup
from urlparse import urlparse


url = "https://www.virustotal.com/vi/domain/yahoo.com/information/"
headers = {"Cookie":"VT_PREFERRED_LANGUAGE=vi; __utma=194538546.702379437.1482145535.1482145535.1482145535.1; __utmb=194538546.7.10.1482145535; __utmc=194538546; __utmz=194538546.1482145535.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1","User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}

r = requests.get(url, headers=headers, verify=True)

if "VirusTotal is trying to prevent scraping and abuse, we are going to bother" not in r.text:

	soup = BeautifulSoup(r.text)
	search_tags = soup.find_all("a", attrs={"target":"_blank","class":None}, href = True)
	for tag in search_tags:
		print tag.string
else:
	print "Captcha_detected"