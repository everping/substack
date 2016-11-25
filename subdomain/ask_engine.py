import re
import urlparse
from engine import EngineThreaded


class AskEngine(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        base_url = 'http://www.ask.com/web?q={query}&page={page_no}&qid=8D6EE6BF52E0C04527E51F64F22C4534&o=0&l=dir' \
                   '&qsrc=998&qo=pagination'
        self.engine_name = "Ask"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 0
        EngineThreaded.__init__(self, base_url, self.engine_name, domain, sub_domains, q=q, silent=silent,
                                verbose=verbose)
        self.q = q
        return

    def extract_domains(self, resp):
        link_regx = re.compile('<p class="web-result-url">(.*?)</p>')
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.sub_domains and subdomain != self.domain:
                    if self.verbose:
                        self._print("%s: %s" % (self.engine_name, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass

        return links_list

    def get_page(self, num):
        return num + 1

    def generate_query(self):
        if self.sub_domains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.sub_domains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)

        return query
