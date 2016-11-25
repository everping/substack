import re
import sys
import os
import multiprocessing
import socket
import functools

from subbrute import subbrute
from utils import subdomain_cmp, is_live, write_file, is_windows
from subdomain.ask_engine import AskEngine
from subdomain.bing_engine import BingEnum
from subdomain.yahoo_engine import YahooEnum
from subdomain.baidu_engine import BaiduEnum
from subdomain.google_engine import GoogleEnum
from subdomain.netcraft_engine import NetcraftEnum
from subdomain.dnsdumpster_engine import DNSdumpster
from subdomain.virustotal_engine import Virustotal
from subdomain.threatcrowd_engine import ThreatCrowd
from subdomain.crtsearch_engine import CrtSearch
from subdomain.passivedns_engine import PassiveDNS
from objects.domain import Domain

if sys.version > '3':
    import urllib.parse as urlparse
else:
    import urlparse

try:
    import requests.packages.urllib3

    requests.packages.urllib3.disable_warnings()
except:
    pass




def main(domain_name, threads, save_file, ports, silent, verbose, enable_brute_force=False):
    brute_force_list = set()
    search_list = set()
    seed_domain = Domain(domain_name)

    if is_windows():
        sub_domains_queue = list()
    else:
        sub_domains_queue = multiprocessing.Manager().list()

    if not seed_domain.is_valid:
        print("Error: Please enter a valid domain")
        return []

    if not silent: print("[-] Enumerating subdomains now for %s" % seed_domain.domain_name)

    if verbose and not silent:
        print("[-] verbosity is enabled, will show the subdomains results in realtime")

    # Start the engines enumeration
    enums = [enum(seed_domain.url, [], q=sub_domains_queue, silent=silent, verbose=verbose) for enum in (BingEnum,)]
    for enum in enums:
        enum.start()
    for enum in enums:
        enum.join()

    subdomains = set(sub_domains_queue)
    for subdomain in subdomains:
        search_list.add(subdomain)

    if enable_brute_force:
        if not silent: print("[-] Starting bruteforce module now using subbrute..")
        record_type = False
        path_to_file = os.path.dirname(os.path.realpath(__file__))
        subs = os.path.join(path_to_file, 'subbrute', 'names.txt')
        resolvers = os.path.join(path_to_file, 'subbrute', 'resolvers.txt')
        process_count = threads
        output = False
        json_output = False
        brute_force_list = subbrute.print_target(seed_domain.domain_name, record_type, subs, resolvers, process_count,
                                                 output, json_output, search_list, verbose)

    subdomains = search_list.union(brute_force_list)

    if subdomains:
        subdomains = sorted(
            subdomains,
            key=functools.cmp_to_key(subdomain_cmp),
        )
        if save_file:
            write_file(save_file, subdomains)

        if not silent:
            print("[-] Total Unique Subdomains Found: %s" % len(subdomains))
            for subdomain in subdomains:
                if is_live(subdomain):
                    print(subdomain + " " + socket.gethostbyname(subdomain))

    return subdomains

import time
a = time.time()
if __name__ == "__main__":
    _domain = "yahoo.com"
    _threads = 30
    _save_file = False
    _ports = False
    _enable_brute_force = False
    _verbose = False
    if _verbose or _verbose is None:
        _verbose = True

    res = main(_domain, _threads, _save_file, _ports, silent=False, verbose=_verbose,
               enable_brute_force=_enable_brute_force)
b = time.time()
print b-a