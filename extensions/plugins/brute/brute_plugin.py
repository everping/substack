from substack.plugins.brute_force_plugin import BruteForcePlugin
from substack.helper.dns import get_authoritative, translate
from substack.helper.utils import PLUGIN_DIRECTORY


class BrutePlugin(BruteForcePlugin):
    def __init__(self):
        BruteForcePlugin.__init__(self)
        self.dict_file = PLUGIN_DIRECTORY + "/brute/data/names.txt"

    def dictionary(self):
        f = open(self.dict_file, 'r')
        content = f.readlines()
        f.close()
        results = []

        name_servers = get_authoritative(self.base_domain.domain_name)
        for i in xrange(len(content)):
            for j in xrange(len(name_servers)):
                result = dict()
                result['pref'] = content[i]
                result['ns'] = name_servers[j]
                results.append(result)

        return results

    def worker(self, args):
        new_domain = args['pref'].strip() + '.' + self.base_domain.domain_name
        if not self.is_existed(new_domain):
            ip = translate(new_domain, args['ns'])
            if ip is not None:
                self.add(new_domain)
