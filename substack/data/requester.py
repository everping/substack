import requests
from substack.data.logger import logger


class Requester:
    """
    This class is based on the requests class.
    I want to replace the requests class by Requester for more effective control HTTP requests
    """

    def __init__(self):
        self._headers = {}
        self._proxies = None

    def set_header(self, headers):
        self._headers = headers

    def set_agent(self, agent):
        self._headers['User-Agent'] = agent

    def set_proxy(self, proxies):
        self._proxies = proxies

    def get(self, url, headers=None):
        if headers is None:
            headers = self._headers

        for i in range(3):
            while True:
                try:
                    return requests.get(url, headers=headers, proxies=self._proxies, timeout=60)
                except requests.exceptions.Timeout:
                    logger.error("It takes a request so long so I must kill it.")
                    logger.info("Trying to reconnect...")
                    continue
                except:
                    logger.error("I don't know why this error occurred")
                    logger.info("Trying to reconnect...")
                    continue
        return None

    def post(self, url, data=None, headers=None):
        if headers is None:
            headers = self._headers

        for i in range(3):
            while True:
                try:
                    return requests.get(url, headers=headers, proxies=self._proxies, data=data, timeout=60)
                except requests.exceptions.Timeout:
                    logger.error("It takes a request so long so I must kill it.")
                    logger.info("Trying to reconnect...")
                    continue
                except:
                    logger.error("I don't know why this error occurred")
                    logger.info("Trying to reconnect...")
                    continue
        return None
