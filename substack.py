import time
from search.engine_factory import EngineFactory
from data.domain import Domain
from data.logger import logger
from config import config


class SubStack:
    def __init__(self):
        self.already_walked = []
        self.engines = []
        self.start_time = 0

    def set_target(self, targets):
        config.save("target", targets)

    def set_mode(self, modes):
        if "discovery" in modes or "bruteforce" in modes:
            config.load("mode")[mode]['active'] = True

        if "discovery" not in modes:
            config.load("mode")["discovery"]['active'] = False
            config.load("mode")["discovery"]['engines'] = []

        if "bruteforce" not in modes:
            config.load("mode")["bruteforce"]['active'] = False

    def set_engine(self, engines_name):
        if config.load("mode")["discovery"]['active'] == True:
            config.load("mode", "discovery")["engines"] = engines_name

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
        targets = [Domain(domain_name) for domain_name in config.load("target")]
        self.engines = [EngineFactory.create(engine_name) for engine_name in
                        config.load("mode")['discovery']['engines']]

        discovered_list = self.discover(targets)
        return discovered_list

    def discover(self, to_walk):
        self.already_walked = to_walk

        while len(to_walk):
            sub_domain_list = []
            for engine in self.engines:
                for domain in to_walk:
                    if self.get_discovery_time() > config.load("timeout"):
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

    def start(self):
        logger.info("Start discovering sub-domains of %s" % ", ".join(config.load("target")))
        self.start_time = time.time()
        self.discover_and_brute_force()


domains = ['garena.com', 'bkav.com']
mode = ["discovery", "bruteforce"]
engines_name = ['Bing', 'Baidu']

sub_stack = SubStack()

sub_stack.set_target(domains)
# sub_stack.set_mode(mode)
# sub_stack.set_engine(engines_name)

sub_stack.start()
