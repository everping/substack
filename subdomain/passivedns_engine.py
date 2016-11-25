import threading
import re
from engine import EngineThreaded

class PassiveDNS(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        base_url = 'http://ptrarchive.com/tools/search.htm?label={domain}'
        self.engine_name = "PassiveDNS"
        self.lock = threading.Lock()
        self.q = q
        self.timeout = 25
        super(PassiveDNS, self).__init__(base_url, self.engine_name, domain, sub_domains, q=q, silent=silent,
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
            self._print(e)
            resp = None

        return self.get_response(resp)

    def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = self.req(url)
        self.extract_domains(resp)
        return self.sub_domains

    def extract_domains(self, resp):
        link_regx = re.compile('<td>(.*?)</td>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                if self.domain not in link:
                    continue
                subdomain = link[:link.find('[')].strip()
                if subdomain not in self.sub_domains and subdomain != self.domain and subdomain.endswith(self.domain):
                    if self.verbose:
                        self._print("%s: %s" % (self.engine_name, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass
