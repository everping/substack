import requests
from config import config


class Requester:
    """
    This class is based on the requests class.
    I want to replace the requests class by Requester for more effective control HTTP requests
    """

    def __init__(self):
        self._headers = None
        self._proxies = None
        self._default()

    def set_header(self, headers):
        self._headers = headers

    def set_proxy(self, proxies):
        self._proxies = proxies

    def get_body(self, url):
        return requests.get(url, headers=self._headers, proxies=self._proxies).text

    def _default(self):
        if config.load('request')['proxy'] != "":
            self.set_proxy(config.load('request')['proxy'])

        if config.load('request')['agent'] != "":
            user_agent = {'User-Agent': config.load('request')['agent']}
            self.set_header(user_agent)


requester = Requester()
