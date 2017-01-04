from substack.helper.dns import get_authoritative, query
from substack.plugins.brute_force_plugin import BruteForcePlugin


class DNSPlugin(BruteForcePlugin):
    """
    This plugin search through all the DNS records of a specific hostname to find all the hidden sub-domains
    """

    def __init__(self):
        BruteForcePlugin.__init__(self)

    def worker(self, args):
        results = query(self.base_domain.domain_name, query_type=args['record'], name_server=args['name_server'])
        for result in results:
            self.add(result['host'])

    def dictionary(self):
        results = []
        authoritative_name_servers = get_authoritative(self.base_domain.domain_name)
        dns_records = ['ANY', 'AXFR', 'IXFR']

        for i in xrange(len(dns_records)):
            for j in xrange(len(authoritative_name_servers)):
                result = dict()
                result['record'] = dns_records[i]
                result['name_server'] = authoritative_name_servers[j]
                results.append(result)
        return results
