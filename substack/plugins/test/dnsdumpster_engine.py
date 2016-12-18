import requests
from urlparse import urlparse
from bs4 import BeautifulSoup

site = "google.com"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0", "Cookie":"csrftoken=xW6DIMrTX9qge6cQuCE1OmZgmGunVinw", "Referer":" https://dnsdumpster.com/"}
payload = {"csrfmiddlewaretoken":"xW6DIMrTX9qge6cQuCE1OmZgmGunVinw","targetip":site}
url = "https://dnsdumpster.com/"

r = requests.post(url, data=payload, headers=header, verify=False)
soup = BeautifulSoup(r.text)

search_tags = soup.find_all('td', attrs={"class":"col-md-4"})
for tag in search_tags:
	domain = tag.contents[0]
	if site in domain:
		print domain