from bs4 import BeautifulSoup
from urlparse import urlparse
import requests, re

url = "https://www.google.com.vn/search?q=site:garena.com&start=30"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"}
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
# print soup
domains = soup.findAll('cite')

for line in domains:
    try:
        url = str(line.string.split()[0])

        if url.startswith("https", 0, 5):
            print urlparse(url).netloc
        else:
            url = "http://" + url
            print urlparse(url).netloc
    except:
        print "somthing was wrong!"
        pass

# url = "https://www.google.com.vn/search?q=site:bkav.com&start=50"
tag_a = soup.findAll('a', attrs={'class': 'fl'})
num_page = tag_a[-1]['aria-label']
print int(num_page.split()[1])
