from objects.domain import Domain


class PiDomain:
    def __init__(self, domain_name):
        self.domain = Domain(domain_name)

    def verify(self):
        pass

    def start(self):
        enums = [enum(self.domain.url, [], q=sub_domains_queue, silent=silent, verbose=verbose) for enum in
                 (BaiduEnum,)]

    for enum in enums:
        enum.discover()
    for enum in enums:
        enum.join()

# domain = "bkav.com"
# pidomain = PiDomain
