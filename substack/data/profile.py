import ConfigParser
import codecs
import os

from substack.data.exceptions import ProfileException
from substack.helper.utils import PROFILE_DIRECTORY, PROFILE_SECTION, PROFILE_EXTENSION


class Profile:
    def __init__(self, profile_name=''):
        self.config = ConfigParser.ConfigParser()
        self.profile_file_name = ''
        self.load(profile_name)

    def load(self, profile_name):
        if not profile_name:
            return

        profile_path = self.get_profile_path(profile_name)
        with codecs.open(profile_path, "rb", 'utf-8') as fp:
            try:
                self.config.readfp(fp)
            except ConfigParser.Error, cpe:
                msg = 'ConfigParser error in profile: "%s". Exception: "%s"'
                raise ProfileException(msg % (profile_name, cpe))
            except Exception, e:
                msg = 'Unknown error in profile: "%s". Exception: "%s"'
                raise ProfileException(msg % (profile_name, e))
            else:
                if not self.get_name():
                    msg = ('The profile with name "%s" does NOT contain a'
                           ' [profile] section with the "name" attribute.')
                    raise ProfileException(msg % (profile_name,))
        self.profile_file_name = profile_path

    def get_profile_path(self, profile_name):
        if not profile_name.endswith(PROFILE_EXTENSION):
            profile_name += PROFILE_EXTENSION

        if os.path.exists(profile_name):
            return profile_name

        for file_name in os.listdir(PROFILE_DIRECTORY):
            if file_name == profile_name:
                real_profile_path = os.path.join(PROFILE_DIRECTORY, profile_name)
                return real_profile_path

    def set_target(self, target):
        """
        Target is a string with form: 'google.com, bing.com'
        """
        section = 'target'
        if section not in self.config.sections():
            self.config.add_section(section)
        self.config.set(section, 'target', target)

    def get_target(self):
        """
        Return a list of targets
        """
        targets = self.get_option_section('target', 'target')
        targets = [target.strip() for target in targets.split(',')]
        return targets

    def set_enabled_plugins(self, plugin_type, plugin_names):
        """
        Set the enabled plugins of type plugin_type.

        :param plugin_type: 'brute_force', 'discovery', etc.
        :param plugin_names: ['bing', 'google'] ...
        :return: None
        """
        # First, get the enabled plugins of the current profile
        current_enabled_plugins = self.get_enabled_plugins(plugin_type)

        for already_enabled_plugin in current_enabled_plugins:
            if already_enabled_plugin not in plugin_names:
                # The plugin was disabled!
                # I should remove the section from the config
                section = '%s.%s' % (plugin_type, already_enabled_plugin)
                self.config.remove_section(section)

        # Now enable the plugins that the user wants to run
        for plugin in plugin_names:
            try:
                self.config.add_section(plugin_type + "." + plugin)
            except ConfigParser.DuplicateSectionError:
                pass

    def get_enabled_plugins(self, plugin_type):
        """
        :return: A list of enabled plugins of type plugin_type
        """
        res = []
        for section in self.config.sections():
            # Section is something like search.bing or bruteforce.subbrute
            try:
                _type, name = section.split('.')
            except:
                pass
            else:
                if _type == plugin_type:
                    res.append(name)
        return res

    def set_misc_settings(self, options):
        """
        Set the misc settings options.
        :param options: a dict
        :return: None
        """
        self.set_option_section('misc-settings', options)

    def get_misc_settings(self, option=None):
        """
        Get the misc settings options.
        :return: The misc settings in an dict
        """
        return self.get_option_section('misc-settings', option)

    def set_http_settings(self, options):
        """
        Set the http settings options.
        :param options: a dict
        :return: None
        """
        self.set_option_section('http-settings', options)

    def get_http_settings(self, option=None):
        return self.get_option_section('http-settings', option)

    def set_name(self, name):
        if PROFILE_SECTION not in self.config.sections():
            self.config.add_section(PROFILE_SECTION)

        self.config.set(PROFILE_SECTION, 'name', name)

    def get_name(self):
        return self.get_option_section(PROFILE_SECTION, 'name')

    def set_desc(self, desc):
        if PROFILE_SECTION not in self.config.sections():
            self.config.add_section(PROFILE_SECTION)

        self.config.set(PROFILE_SECTION, 'description', desc)

    def get_desc(self):
        return self.get_option_section(PROFILE_SECTION, 'description')

    def save(self, file_name=''):
        """
        Saves the profile to file_name.
        :return: None
        """
        if not self.profile_file_name:
            if not file_name:
                raise ProfileException('Error saving profile, profile file name is required.')
            else:
                # The user's specified a file_name!
                if not file_name.endswith(PROFILE_EXTENSION):
                    file_name += PROFILE_EXTENSION

            if os.path.sep not in file_name:
                file_name = os.path.join(PROFILE_DIRECTORY, file_name)
            self.profile_file_name = file_name

        try:
            file_handler = open(self.profile_file_name, 'w')
        except:
            msg = 'Failed to open profile file: "%s"'
            raise ProfileException(msg % self.profile_file_name)
        else:
            self.config.write(file_handler)

    def set_option_section(self, section, options):
        """
        Set the section options.

        :param section: The section name
        :param options: an OptionList
        :return: None
        """

        if section not in self.config.sections():
            self.config.add_section(section)

        for option in options:
            self.config.set(section, option, options[option])

    def get_option_section(self, section, option=None):
        """
        Get value of option in a section
        If option is not None, return value of this option
        If option is None, return a dict includes all option and their value
        """
        if option is not None:
            try:
                result = self.config.get(section, option)
                if result.strip() == "":
                    result = None
            except KeyError:
                return None

        else:
            result = {}
            try:
                profile_options = self.config.options(section)
            except ConfigParser.NoSectionError as e:
                msg = 'Could not find section "%s"'
                raise ProfileException(msg % section)

            for _option in profile_options:
                value = self.config.get(section, _option)
                result[_option] = value

        return result
