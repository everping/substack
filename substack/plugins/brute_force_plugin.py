from substack.plugins.sub_domain_plugin import SubDomainPlugin


class BruteForcePlugin(SubDomainPlugin):
    """
    This plugin brute force sub-domains from a list prefix
    """

    def __init__(self):
        SubDomainPlugin.__init__(self)

    def get_type(self):
        return "brute"

    def worker(self, args):
        """
        The real worker of this plugin
        """
        msg = 'Plugin is not implementing required method worker'
        raise NotImplementedError(msg)

    def dictionary(self):
        """
        Generate the dictionary that used to worker
        """
        msg = 'Plugin is not implementing required method dictionary'
        raise NotImplementedError(msg)
