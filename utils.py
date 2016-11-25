import socket
import sys
import argparse


def is_windows():
    return sys.platform.startswith('win')

def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumerate it's subdomains", required=True)
    parser.add_argument('-b', '--bruteforce', help='Enable the subbrute bruteforce module', nargs='?', default=False)
    parser.add_argument('-p', '--ports', help='Scan the found subdomains against specified tcp ports')
    parser.add_argument('-v', '--verbose', help='Enable Verbosity and display results in realtime', nargs='?',
                        default=False)
    parser.add_argument('-t', '--threads', help='Number of threads to use for subbrute bruteforce', type=int,
                        default=30)
    parser.add_argument('-o', '--output', help='Save the results to text file')
    return parser.parse_args()


def write_file(filename, subdomains):
    # saving subdomains results to output file
    print("%s[-] Saving results to file: %s%s%s%s" % (Y, W, R, filename, W))
    with open(str(filename), 'wt') as f:
        for subdomain in subdomains:
            f.write(subdomain + "\r\n")


def subdomain_cmp(d1, d2):
    """cmp function for subdomains d1 and d2.

    This cmp function orders subdomains from the top-level domain at the right
    reading left, then moving '^' and 'www' to the top of their group. For
    example, the following list is sorted correctly:

    [
        'example.com',
        'www.example.com',
        'a.example.com',
        'www.a.example.com',
        'b.a.example.com',
        'b.example.com',
        'example.net',
        'www.example.net',
        'a.example.net',
    ]

    """
    d1 = d1.split('.')[::-1]
    d2 = d2.split('.')[::-1]

    val = 1 if d1 > d2 else (-1 if d1 < d2 else 0)
    if ((len(d1) < len(d2)) and
            (d1[-1] == 'www') and
            (d1[:-1] == d2[:len(d1) - 1])):
        val = -1
    elif ((len(d1) > len(d2)) and
              (d2[-1] == 'www') and
              (d1[:len(d2) - 1] == d2[:-1])):
        val = 1
    elif d1[:-1] == d2[:-1]:
        if d1[-1] == 'www':
            val = -1
        elif d2[-1] == 'www':
            val = 1
    return val


def is_live(domain):
    ret = True
    try:
        socket.gethostbyname(domain)
    except:
        ret = False
    return ret
