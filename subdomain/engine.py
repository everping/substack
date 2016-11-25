import sys
import multiprocessing
import requests
import threading

if sys.version > '3':
    import urllib.parse as urlparse
else:
    import urlparse


class Engine(object):
    def __init__(self, base_url, engine_name, domain, sub_domains=None, silent=False, verbose=True):
        sub_domains = sub_domains or []
        self.domain = urlparse.urlparse(domain).netloc
        self.session = requests.Session()
        self.sub_domains = []
        self.timeout = 10
        self.base_url = base_url
        self.engine_name = engine_name
        self.silent = silent
        self.verbose = verbose
        self.print_banner()
        self.MAX_DOMAINS = 0
        self.MAX_PAGES = 0

    def _print(self, text):
        if not self.silent:
            print(text)
        return

    def print_banner(self):
        """ subclass can override this if they want a fancy banner :)"""
        self._print("[-] Searching now in %s.." % self.engine_name)
        return

    def send_req(self, query, page_no=1):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-GB,en;q=0.5',
                   'Accept-Encoding': 'gzip, deflate',
                   'Connection': 'keep-alive'
                   }

        url = self.base_url.format(query=query, page_no=page_no)
        print url
        try:
            resp = self.session.get(url, headers=headers, timeout=self.timeout)
        except Exception as e:
            resp = None
        return self.get_response(resp)

    def get_response(self, response):
        if response is None:
            return 0
        if hasattr(response, "text"):
            return response.text
        else:
            return response.content

    def check_max_sub_domains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False
        return num >= self.MAX_PAGES

    # Override
    def extract_domains(self, resp):
        """ child class should override this function """
        return

    # override
    def check_response_errors(self, resp):
        """ child class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumerators require sleeping to avoid bot detections like Google enumerator"""
        return

    def generate_query(self):
        """ child class should override this function """
        return

    def get_page(self, num):
        """ child class that user different pagination counter should override this function """
        return num + 10

    def enumerate(self, alt_query=False):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            query = self.generate_query()
            print query
            count = query.count(self.domain)  # finding the number of sub domains found so far

            print count

            # if they we reached the maximum number of sub domains in search query
            # then we should go over the pages
            if self.check_max_sub_domains(count):
                page_no = self.get_page(page_no)
                print page_no

            if self.check_max_pages(page_no):  # maximum pages for Google to avoid getting blocked
                return self.sub_domains
            resp = self.send_req(query, page_no)

            # check if there is any error occurred
            if not self.check_response_errors(resp):
                return self.sub_domains
            links = self.extract_domains(resp)
            print links
            # if the previous page hyperlinks was the similar to the current one,
            # then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)

                # make another retry maybe it isn't the last page
                if retries >= 3:
                    return self.sub_domains

            prev_links = links
            self.should_sleep()

        return self.sub_domains


class EngineThreaded(multiprocessing.Process, Engine):
    def __init__(self, base_url, engine_name, domain, sub_domains=None, q=None, lock=threading.Lock(), silent=False,
                 verbose=True):
        sub_domains = sub_domains or []
        Engine.__init__(self, base_url, engine_name, domain, sub_domains, silent=silent, verbose=verbose)
        multiprocessing.Process.__init__(self)
        self.lock = lock
        self.q = q
        return

    def run(self):
        domain_list = self.enumerate()
        for domain in domain_list:
            self.q.append(domain)
