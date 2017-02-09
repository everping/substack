import argparse
import sys

from substack.data.profile import Profile
from substack.substack_core import SubStack


def parser_error(msg):
    print("Usage: python " + sys.argv[0] + " [Options] \nUse -h for help")
    print("Error: " + msg)
    sys.exit()


def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d google.com")
    parser.add_argument('-d', '--domain',
                        help="The domain that we want to search its sub-domain. If you are looking for many different"
                             " domains, separate them by commas",
                        required=True)
    parser.add_argument('-v', '--version', help='Check version of Substack', nargs='?', default=False)
    return parser.parse_args()


def main():
    args = parse_args()
    domain = args.domain
    print domain

    # profile = Profile("empty")
    # profile.set_target("bkav.com")
    #
    # sub_stack = SubStack()
    # sub_stack.set_profile(profile)
    #
    # sub_stack.start()


def start(domain):
    pass


if __name__ == "__main__":
    main()
    # print parse_args()
