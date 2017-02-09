from bs4 import BeautifulSoup
import requests
import json

target = "garena.com"
url = "https://www.threatcrowd.org/searchApi/v2/domain/report/?domain=" + target
print url
header = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Accept-Language': 'en-GB,en;q=0.5',
          'Accept-Encoding': 'gzip, deflate',
          'Cookie': '__cfduid=d9aa25d654e7bb0e61da2b7540ff0390d1483039889; FirstVisit=No; _ga=GA1.2.724560729.1483039951',
          'Host': 'www.threatcrowd.org',
          }

r = requests.get(url, headers=header)

for tem in (json.loads(r.text)['subdomains']):
    print tem
