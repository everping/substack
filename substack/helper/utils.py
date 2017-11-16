from os import pardir
from os.path import abspath, join, dirname, realpath

PROFILE_SECTION = 'profile'
PROFILE_EXTENSION = '.pss'
ROOT_DIRECTORY = abspath(join(dirname(realpath(__file__)), pardir, pardir))
PROFILE_DIRECTORY = join(ROOT_DIRECTORY, 'extensions', 'profiles')
PLUGIN_DIRECTORY = join(ROOT_DIRECTORY, 'extensions', 'plugins')
LOG_PATH = join(ROOT_DIRECTORY, 'log', 'substack.log')
OUT_PATH = join(ROOT_DIRECTORY, 'out')

STATE_NOT_FOUND = 'not_found'
STATE_BLOCKED = 'blocked'
STATE_OK = 'ok'
