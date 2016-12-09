import time

from substack.data.domain import Domain
from substack.data.logger import logger
from substack.data.requester import Requester
from substack.plugins.base.plugin_factory import PluginFactory


class SubStack:
    def __init__(self):
        self.already_walked = []
        self.plugin_types = ['search', 'port']
        self.plugins = {}
        self.start_time = 0
        self.profile = None
        self.targets = []
        for plugin_type in self.plugin_types:
            self.plugins[plugin_type] = []

    def init_requester(self):
        requester = Requester()
        agent = self.profile.get_http_settings("agent")
        proxy = self.profile.get_http_settings("proxy")

        if agent is not None:
            requester.set_agent(agent)

        if proxy is not None:
            requester.set_proxy(proxy)

        return requester

    def init_plugin(self):
        for plugin_type in self.plugin_types:
            for plugin_name in self.profile.get_enabled_plugins(plugin_type):
                plugin = PluginFactory(plugin_name, plugin_type, self.init_requester()).create()
                if plugin is not None:
                    self.plugins[plugin_type].append(plugin)

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

        discovered_list = self.discover()
        return discovered_list

    def discover(self):
        self.already_walked = self.targets
        to_walk = self.targets

        while len(to_walk):
            sub_domain_list = []
            for plugin in self.plugins["search"]:
                for domain in to_walk:
                    if self.get_discovery_time() > int(self.profile.get_misc_settings("max_discovery_time")):
                        logger.error("Stopped since overtime")
                        break
                    else:
                        engine_result = plugin.discover(domain)
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

    # def scan_port(self, domains):
    #     already_scanned = []
    #     m = MxToolboxEngine()
    #     for domain in domains:
    #         if domain.ip not in already_scanned:
    #             m.scan(domain)
    #             already_scanned.append(domain.ip)

    def start(self):
        self.start_time = time.time()
        self.init_plugin()
        self.targets = [Domain(domain_name) for domain_name in self.profile.get_target()]
        sub_domains = self.discover_and_brute_force()
        # open_ports = self.scan_port(sub_domains)
