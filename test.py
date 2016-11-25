import requests
from bs4 import BeautifulSoup

query = "site:bkav.com"

base_url = "http://www.baidu.com/s?wd={query}&pn={page}"


def get_total_page():
    url = base_url.format(query=query, page=0)
    r = requests.get(url)

    # http://stackoverflow.com/a/25661119/6805843
    soup = BeautifulSoup(r.text, "html5lib")
    a_tags = soup.find_all('a', class_="c-showurl")
    for a in a_tags:
        print a.string
    # return div_page.find('strong').find_all('span')[1].string

get_total_page()