import argparse
import sys

from substack.data.profile import Profile
from substack.substack_core import SubStack


def parser_error():
    print("Usage: python " + sys.argv[0] + " [Options] \nUse -h for help")
    sys.exit()


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.add_argument('-d', '--domain',
                        help="The domain that we want to search its sub")
    parser.add_argument('-v', '--version', help='Check version of Substack', nargs='?', default=False)
    return parser.parse_args()


def version():
    print 'v1.0'


def main():
    args = parse_args()
    domain = args.domain
    _version = args.version

    if _version is not False:
        version()

    if domain is None:
        parser_error()

    profile = Profile("empty")
    profile.set_target(domain)

    sub_stack = SubStack()
    sub_stack.set_profile(profile)

    sub_stack.start()


if __name__ == "__main__":
    main()
