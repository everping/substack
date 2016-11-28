import requests
from config import config


class Requester:
    def __init__(self):
        self.headers = None
        self.proxies = None
        self.config()

    def set_header(self, headers):
        self.headers = headers

    def set_proxy(self, proxies):
        self.proxies = proxies

    def get_body(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxies).text

    def config(self):
        if config['request']['proxy'] != "":
            self.set_proxy(config['request']['proxy'])

        if config['request']['agent'] != "":
            user_agent = {'User-Agent': config['request']['agent']}
            self.set_header(user_agent)


requester = Requester()

# a = Requester()
# a.config()

# proxies = {
#     'http': 'http://127.0.0.1:3333'
# }
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
# }
#
# a.set_proxy(proxies)
# a.set_header(headers)
# print a.get_body("http://bkav.com")
