import re
import urlparse

from engine import EngineThreaded


class BingEnum(EngineThreaded):
    def __init__(self, domain, sub_domains=None, q=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        base_url = 'https://www.bing.com/search?q={query}&go=Submit&first={page_no}'
        self.engine_name = "Bing"
        self.MAX_DOMAINS = 30
        self.MAX_PAGES = 0
        EngineThreaded.__init__(self, base_url, self.engine_name, domain, sub_domains, q=q, silent=silent)
        self.q = q
        self.verbose = verbose
        return

    def extract_domains(self, resp):
        link_regx = re.compile('<li class="b_algo"><h2><a href="(.*?)"')
        link_regx2 = re.compile('<div class="b_title"><h2><a href="(.*?)"')
        try:
            links = link_regx.findall(resp)
            links2 = link_regx2.findall(resp)
            links_list = links + links2

            for link in links_list:
                link = re.sub('<(\/)?strong>|<span.*?>|<|>', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.sub_domains and subdomain != self.domain:
                    if self.verbose:
                        self._print("%s: %s" % (self.engine_name, subdomain))
                    self.sub_domains.append(subdomain.strip())
        except Exception as e:
            pass

        # print links_list

        return links_list

    def generate_query(self):
        if self.sub_domains:
            fmt = 'domain:{domain} -www.{domain} -{found}'
            found = ' -'.join(self.sub_domains[:self.MAX_DOMAINS])
            query = fmt.format(domain=self.domain, found=found)
        else:
            query = "domain:{domain} -www.{domain}".format(domain=self.domain)
        return query
