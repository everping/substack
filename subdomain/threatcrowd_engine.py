import threading
from engine import EngineThreaded

class ThreatCrowd(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
        self.engine_name = "ThreatCrowd"
        self.lock = threading.Lock()
        self.q = q
        self.timeout = 20
        super(ThreatCrowd, self).__init__(base_url, self.engine_name, domain, sub_domains, q=q, silent=silent,
                                          verbose=verbose)
        return

    def req(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/40.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-GB,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   }

        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
        except Exception as e:
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.sub_domains

    def extract_domains(self, resp):
        try:
            import json
        except Exception as e:
            self._print(e)
            return

        try:
            links = json.loads(resp)['subdomains']
            for link in links:
                subdomain = link.strip()
                if not subdomain.endswith(self.domain):
                    continue
                if subdomain not in self.sub_domains and subdomain != self.domain:
                    if self.verbose:
                        self._print("%s: %s" % (self.engine_name, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass
