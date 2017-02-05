from bs4 import BeautifulSoup
import requests
from urlparse import urlparse

site = "garena.com"
url = "https://crt.sh/?q=%25." + site
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}

content = requests.get(url,headers=headers).text
soup = BeautifulSoup(content, "html5lib")

search = soup.find_all("td", attrs={"class":"outer"})
for i in search[1].find_all("td", attrs={"style":None,"href":None}):
	if not i.findChildren():
		try:
			print i.string
		except:
			pass