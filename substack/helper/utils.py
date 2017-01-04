from os import pardir
from os.path import abspath, join, dirname, realpath

PROFILE_SECTION = 'profile'
PROFILE_EXTENSION = '.pss'
ROOT_DIRECTORY = abspath(join(dirname(realpath(__file__)), pardir, pardir))
PROFILE_DIRECTORY = join(ROOT_DIRECTORY, 'extensions', 'profiles')
PLUGIN_DIRECTORY = join(ROOT_DIRECTORY, 'extensions', 'plugins')
LOG_PATH = join(ROOT_DIRECTORY, 'log', 'substack.log')
