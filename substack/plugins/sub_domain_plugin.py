import threading
from substack.data.domain import Domain
from substack.plugins.plugin import Plugin
from substack.data.logger import logger
from substack.data.exceptions import PluginException
from multiprocessing.dummy import Pool as ThreadPool


class SubDomainPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self)
        self.sub_domains = []
        self.max_page = None
        self.lock = threading.Lock()
        self.max_worker = 50

    def get_type(self):
        return "sub"

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

    def discover(self, domain):
        """
        This is the main method, it pass domain_name parameter
        and returns a list of the sub-domain found by the search engine
        """
        try:
            logger.info("Plugin %s has been activated" % self.get_name())
            self.base_domain = domain

            _dict = self.dictionary()
            pool = ThreadPool(self.max_worker)
            pool.map(self.worker, _dict)
            pool.close()
            pool.join()

            return self.sub_domains
        except:
            msg = "Error occurred with plugin %s " % self.get_name()
            raise PluginException(msg)

    def dictionary(self):
        """
        Generate the dictionary that used to work with worker
        """
        msg = 'Plugin is not implementing required method dictionary'
        raise NotImplementedError(msg)

    def worker(self, args):
        """
        The real worker of this plugin
        """
        msg = 'Plugin is not implementing required method worker'
        raise NotImplementedError(msg)
