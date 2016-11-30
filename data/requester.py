import requests
from config import config
from logger import logger


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
        try:
            return requests.get(url, headers=self._headers, proxies=self._proxies, timeout=60).text
        except requests.exceptions.Timeout:
            logger.error("It takes a request so long so I must kill it")
        except Exception as e:
            logger.error("I don't know why this error occurred, so I log it")
            logger.error("My URL: %s" % url)
            logger.error("And trace back exception is bellow")
            logger.error(e.message)

    def _default(self):
        if config.load('request')['proxy'] != "":
            self.set_proxy(config.load('request')['proxy'])

        if config.load('request')['agent'] != "":
            user_agent = {'User-Agent': config.load('request')['agent']}
            self.set_header(user_agent)


requester = Requester()
