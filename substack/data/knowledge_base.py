import threading
from substack.data.domain import Domain


class KnowledgeBase:
    def __init__(self):
        self.sub_domains = []
        self._sub_lock = threading.Lock()

    def is_existed(self, sub_domain_name):
        """
        Check if this domain exist in result list
        """
        for domain in self.sub_domains:
            if domain.domain_name == sub_domain_name:
                return True
        return False

    def add_sub_domain(self, sub_domain_name):
        """
        Add the sub-domain to the result list
        """
        self._sub_lock.acquire()

        if self.is_existed(sub_domain_name):
            self._sub_lock.release()
            return

        try:
            sub_domain = Domain(sub_domain_name)
            sub_domain.save_info("domain_found_by", self.get_name())
            if sub_domain.is_live():
                self.sub_domains.append(sub_domain)
        finally:
            self._sub_lock.release()
