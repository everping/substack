from substack.data.domain import Domain
from substack.data.logger import logger
from substack.data.requester import Requester
from substack.data.knowledge_base import KnowledgeBase
from substack.plugins.plugin_factory import PluginFactory


class SubStack:
    def __init__(self):
        self.plugins = {'search': [], 'brute': []}
        self.profile = None
        self.targets = []
        self.kb = KnowledgeBase()

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
        requester = self.init_requester()

        for plugin_type in self.plugins:
            for plugin_name in self.profile.get_enabled_plugins(plugin_type):
                plugin = PluginFactory(plugin_name, plugin_type, requester).create()
                if plugin is not None:
                    self.plugins[plugin_type].append(plugin)

    def set_profile(self, profile):
        self.profile = profile

    def sub(self):
        logger.info("Start finding sub-domains of %s" % self.profile.get_target())
        self.kb.set_sub_domains(self.targets)
        to_walk = self.targets
        sub_plugins = self.plugins["search"] + self.plugins["brute"]
        while len(to_walk):
            sub_domain_list = []
            new_domain = []

            for plugin in sub_plugins:
                for domain in to_walk:
                    engine_result = plugin.discover(domain)
                    for sd in engine_result:
                        sub_domain_list.append(sd)

            for domain in sub_domain_list:
                if self.kb.add_sub_domain(domain):
                    new_domain.append(domain)

            to_walk = new_domain

        return self.kb.get_sub_domains()

    def find_open_ports(self):
        logger.info("Start finding open ports")

        for plugin in self.plugins['port']:
            already_scanned = []
            for domain in self.kb.get_sub_domains():
                if domain.ip not in already_scanned:
                    open_ports = plugin.scan(domain)
                    self.kb.add_open_ports(domain, open_ports)

                logger.info(
                    "%s (%s) open ports: %s" % (
                        domain.domain_name, domain.ip, ", ".join([str(port) for port in domain.get_open_ports()])))

    def start(self):
        import time
        a = time.time()
        self.init_plugin()
        self.targets = [Domain(domain_name) for domain_name in self.profile.get_target()]
        self.sub()
        print time.time() - a
        # self.find_open_ports()
