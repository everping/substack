import os

PROFILE_SECTION = 'profile'
PROFILE_EXTENSION = '.pss'
PROFILE_DIRECTORY = 'D:\Everping\Work\Projects\substack\profiles'
LOG_PATH = 'D:\Everping\Work\Projects\substack\log\substack.log'


def get_root_dir():
    pwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(os.path.join(pwd, os.pardir, os.pardir))


def get_plugin_dir():
    return os.path.join(get_root_dir(), "substack", "plugins")