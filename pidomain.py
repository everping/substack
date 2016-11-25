import time
from search.bing_engine import BingEngine

a = time.time()

_domain = "bkav.com"

b = BingEngine()
# while 1:
subs = b.discover(_domain)
#     print '.'

# if subs.__len__() != 7:
for d in subs:
    print d.domain_name
    # break  # print b.discover(_domain).__len__()
b = time.time()
print b - a
