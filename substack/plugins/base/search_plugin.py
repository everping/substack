import threading

from substack.data.logger import logger
from substack.data.domain import Domain
from substack.plugins.base.plugin import Plugin


class SearchPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.sub_domains = []
        self.max_page = None
        self.lock = threading.Lock()

    def get_type(self):
        return "search"

    def is_existed(self, sub_domain_name):
        """
        Check if this domain exist in result list
        """
        for domain in self.sub_domains:
            if domain.domain_name == sub_domain_name:
                return True
        return False

    def add(self, sub_domain_name):
        """
        Add the sub-domain to the result list
        """
        self.lock.acquire()

        if self.is_existed(sub_domain_name):
            self.lock.release()
            return

        try:
            sub_domain = Domain(sub_domain_name)
            sub_domain.save_info("domain_found_by", self.get_name())
            if sub_domain.is_live():
                self.sub_domains.append(sub_domain)
        finally:
            self.lock.release()

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

    def extract(self, result_url):
        """
        Parse the response of the result_url to looking for sub-domain.
        Then add them to self.sub_domains.
        """
        msg = 'Plugin is not implementing required method extract'
        raise NotImplementedError(msg)

    def discover(self, domain):
        """
        This is the main method, it pass domain_name parameter
        and returns a list of the sub-domain found by the search engine
        """
        self.base_domain = domain
        total_pages = self.get_total_page()

        threads = []
        for i in xrange(total_pages):
            url = self.base_url.format(query=self.get_query(), page=self.get_page_no(i))
            logger.info("Requesting to %s" % url)
            thread = threading.Thread(target=self.extract, args=(url,))

            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return self.sub_domains
