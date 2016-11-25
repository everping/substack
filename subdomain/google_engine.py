import re
import urlparse
import time

from engine import EngineThreaded


class GoogleEnum(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        base_url = "https://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0"
        self.engine_name = "Google"
        self.MAX_DOMAINS = 11
        self.MAX_PAGES = 200
        super(GoogleEnum, self).__init__(base_url, self.engine_name, domain, sub_domains, q=q, silent=silent,
                                         verbose=verbose)
        self.q = q

    def extract_domains(self, resp):
        link_regex = re.compile('<cite.*?>(.*?)<\/cite>')
        try:
            links_list = link_regex.findall(resp)
            for link in links_list:
                link = re.sub('<span.*>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain and subdomain not in self.sub_domains and subdomain != self.domain:
                    if self.verbose:
                        self._print("%s: %s" % (self.engine_name, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass
        return links_list

    def check_response_errors(self, resp):
        if 'Our systems have detected unusual traffic' in resp:
            self._print("[!] Error: Google probably now is blocking our requests")
            self._print("[~] Finished now the Google Enumeration ...")
            return False
        return True

    def should_sleep(self):
        time.sleep(5)
        return

    def generate_query(self):
        if self.sub_domains:
            fmt = 'site:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.sub_domains[:self.MAX_DOMAINS - 2])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -www.{domain}".format(domain=self.domain)
        return query
