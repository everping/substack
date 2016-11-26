import time
from search.engine_factory import EngineFactory
from objects.domain import Domain


class SubStack:
    def __init__(self):
        self.already_walked = []
        self.engines = []
        self.timeout = None
        self.start_time = 0
        self.target_domain = None

    def set_target(self, domain_name):
        self.target_domain = Domain(domain_name)

    def set_engine(self, engines_name):
        self.engines = [EngineFactory.create(engine_name) for engine_name in engines_name]

    def set_timeout(self, timeout):
        self.timeout = timeout

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
        seed = [self.target_domain]
        discovered_list = self.discover(seed)
        return discovered_list

    def discover(self, to_walk):
        self.already_walked = to_walk

        while len(to_walk):
            sub_domain_list = []
            for engine in self.engines:
                for domain in to_walk:
                    if self.get_discovery_time() > self.timeout:
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
                    print 'New domain found by %s: %s' % (domain.meta_data['found_by'], domain.domain_name)

            to_walk = new_domain
        return self.already_walked

    def start(self):
        self.start_time = time.time()
        self.discover_and_brute_force()


domain = "garena.com"
engines_name = ['Bing', 'Baidu']

sub_stack = SubStack()
sub_stack.set_target(domain)
sub_stack.set_engine(engines_name)
sub_stack.set_timeout(300)
sub_stack.start()
