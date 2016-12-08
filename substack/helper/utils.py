import os


def get_root_dir():
    pwd = os.path.dirname(os.path.realpath(__file__))
    print pwd
    print  os.path.abspath(os.path.join(pwd, os.pardir, os.pardir))

get_root_dir()

# PROFILE_SECTION = 'profile'
# PROFILE_EXTENSION = '.pss'
#
# PROFILE_DIRECTORY = os.path.join(get_root_dir(), 'profiles')
# PLUGIN_DIRECTORY = os.path.join(get_root_dir(), 'substack', 'plugins')
# LOG_PATH = os.path.join(get_root_dir(), 'log', 'substack.log')
