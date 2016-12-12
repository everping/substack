from substack.data.domain import Domain
from substack.data.logger import logger
from substack.data.requester import Requester
from substack.data.knowledge_base import KnowledgeBase
from substack.plugins.base.plugin_factory import PluginFactory


class SubStack:
    def __init__(self):
        self.plugin_types = ['search', 'port']
        self.plugins = {}
        self.start_time = 0
        self.profile = None
        self.targets = []
        self.kb = KnowledgeBase()
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
                plugin = PluginFactory(plugin_name, plugin_type, self.init_requester(), self.kb).create()
                if plugin is not None:
                    self.plugins[plugin_type].append(plugin)

    def set_profile(self, profile):
        self.profile = profile

    def verify(self):
        pass

    def find_sub_domains(self):
        logger.info("Start finding sub-domains of %s" % self.profile.get_target())
        searched_list = self.search()
        return searched_list

    def search(self):
        self.kb.set_sub_domains(self.targets)

        to_walk = self.targets

        while len(to_walk):
            sub_domain_list = []
            new_domain = []

            for plugin in self.plugins["search"]:
                for domain in to_walk:
                    engine_result = plugin.discover(domain)
                    for i in engine_result:
                        sub_domain_list.append(i)

            for domain in sub_domain_list:
                if self.kb.add_sub_domain(domain):
                    new_domain.append(domain)
                    logger.info(
                        'New domain was found by %s: %s' % (domain.meta_data['domain_found_by'], domain.domain_name))

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
        self.init_plugin()
        self.targets = [Domain(domain_name) for domain_name in self.profile.get_target()]
        self.find_sub_domains()
        # self.find_open_ports()
