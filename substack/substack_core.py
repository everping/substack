import time

from substack.data.domain import Domain
from substack.data.logger import logger
from substack.data.requester import Requester
from substack.plugins.search.engine_factory import EngineFactory
from substack.plugins.port.mxtoolbox_engine import MxToolboxEngine


class SubStack:
    def __init__(self):
        self.already_walked = []
        self.engines = []
        self.start_time = 0
        self.profile = None

    def make_requester(self):
        requester = Requester()
        agent = self.profile.get_http_settings("agent")
        proxy = self.profile.get_http_settings("proxy")

        if agent is not None:
            requester.set_agent(agent)

        if proxy is not None:
            requester.set_proxy(proxy)

        return requester

    def set_profile(self, profile):
        self.profile = profile

    def is_existed(self, sub_domain):
        for domain in self.already_walked:
            if domain.domain_name == sub_domain.domain_name:
                return True
        return False

    def verify(self):
        pass

    def get_discovery_time(self):
        now = time.time()
        diff = now - self.start_time
        return diff

    def discover_and_brute_force(self):
        logger.info("Start finding sub-domains of %s" % self.profile.get_target())

        targets = [Domain(domain_name) for domain_name in self.profile.get_target()]

        for search_engine_name in self.profile.get_enabled_plugins("search"):
            self.engines.append(EngineFactory.create(search_engine_name, self.make_requester()))

        discovered_list = self.discover(targets)
        return discovered_list

    def discover(self, to_walk):
        self.already_walked = to_walk

        while len(to_walk):
            sub_domain_list = []
            for engine in self.engines:
                for domain in to_walk:
                    if self.get_discovery_time() > int(self.profile.get_misc_settings("max_discovery_time")):
                        logger.error("Stopped since overtime")
                        break
                    else:
                        engine_result = engine.discover(domain)
                        for i in engine_result:
                            sub_domain_list.append(i)

            new_domain = []

            for domain in sub_domain_list:
                if not self.is_existed(domain):
                    new_domain.append(domain)
                    self.already_walked.append(domain)
                    logger.info('New domain found by %s: %s' % (domain.meta_data['found_by'], domain.domain_name))

            to_walk = new_domain
        return self.already_walked

    def setup_engine(self):
        for search_engine_name in self.profile.get_enabled_plugins("search"):
            self.engines.append(EngineFactory.create(search_engine_name, self.make_requester()))


    def scan_port(self, domains):
        already_scanned = []
        m = MxToolboxEngine()
        for domain in domains:
            if domain.ip not in already_scanned:
                m.scan(domain)
                already_scanned.append(domain.ip)

    def start(self):
        self.start_time = time.time()
        sub_domains = self.discover_and_brute_force()
        open_ports = self.scan_port(sub_domains)



