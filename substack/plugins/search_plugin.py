import urllib
from urlparse import urlparse
from substack.plugins.sub_domain_plugin import SubDomainPlugin
from substack.helper.utils import STATE_BLOCKED, STATE_NOT_FOUND, STATE_OK


class SearchPlugin(SubDomainPlugin):
    def __init__(self):
        SubDomainPlugin.__init__(self)
        self.max_page = None
        self.max_worker = 20
        self.messages = {
            STATE_NOT_FOUND: [],
            STATE_BLOCKED: []
        }

    def get_type(self):
        return "search"

    def get_query(self):
        """
        This method return dork for searching sub-domain corresponding to each search engine
        """
        msg = 'Plugin is not implementing required method get_query'
        raise NotImplementedError(msg)

    def get_page_no(self, seed):
        """
        Each search engine has a different page numbering for search results,
        this method returns the number corresponding to the order page result
        """
        msg = 'Plugin is not implementing required method get_page_no'
        raise NotImplementedError(msg)

    def get_total_page(self):
        """
        :return: This method returns an integer that is the number of pages found by the search engine
        """
        msg = 'Plugin is not implementing required method get_total_page'
        raise NotImplementedError(msg)

    def worker(self, result_url):
        self.extract(result_url)

    def extract(self, result_url):
        """
        Parse the response of the result_url to looking for sub-domain.
        Then add them to self.sub_domains.
        """
        msg = 'Plugin is not implementing required method extract'
        raise NotImplementedError(msg)

    def has_error(self, response):
        """
        If a plugin meet any error, it must override this method
        """
        return False

    def state(self, response):
        for msg in self.messages[STATE_NOT_FOUND]:
            if msg in response:
                return STATE_NOT_FOUND

        for msg in self.messages[STATE_BLOCKED]:
            if msg in response:
                return STATE_BLOCKED

        return STATE_OK

    def was_blocked(self, response):
        if self.state(response) == STATE_BLOCKED:
            return True
        return False

    def was_not_found(self, response):
        if self.state(response) == STATE_NOT_FOUND:
            return True
        return False

    @staticmethod
    def parse_domain_name(my_url):
        my_url = urllib.unquote(my_url)
        if not my_url.startswith("http://") and not my_url.startswith("https://"):
            my_url = "http://" + my_url

        return urlparse(my_url).netloc

    def dictionary(self):
        """
        We create a list of urls that based on this Search Engine
        ;:return: a list instance
        """
        try:
            urls = []
            total_pages = self.get_total_page()
            for i in xrange(total_pages):
                url = self.base_url.format(query=self.get_query(), page=self.get_page_no(i))
                urls.append(url)
            return urls
        except:
            print self.get_name()
            raise
