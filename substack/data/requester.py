import requests

from substack.data.exceptions import RequesterException


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

    def get(self, url):
        try:
            return requests.get(url, headers=self._headers, proxies=self._proxies)
        except requests.exceptions.Timeout:
            raise RequesterException("It takes a request so long so I must kill it")
        except:
            msg = "I don't know why this error occurred, so I log it\nMy URL: %s"
            raise RequesterException(msg % url)

    def post(self, url, data=None):
        try:
            return requests.get(url, headers=self._headers, proxies=self._proxies, data=data, timeout=60)
        except requests.exceptions.Timeout:
            raise RequesterException("It takes a request so long so I must kill it")
        except:
            msg = "I don't know why this error occurred, so I log it\nMy URL: %s"
        raise RequesterException(msg % url)


    def custom_post(self, url, header, data):
        try:
            return requests.post(url, headers=header, proxies=self._proxies, data=data, timeout=60)
        except requests.exceptions.Timeout:
            raise RequesterException("It takes a request so long so I must kill it")
        except:
            msg = "I don't know why this error occurred, so I log it\nMy URL: %s"
        raise RequesterException(msg % url)
