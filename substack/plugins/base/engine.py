class Engine:
    def __init__(self):
        self.requester = None
        self.base_url = None

    def get_name(self):
        return self.__class__.__name__

    def get_type(self):
        return 'engine'

    def set_requester(self, requester):
        self.requester = requester
        if self.requester is not None:
            self.setup_http()

    def setup_http(self):
        """
        I think we will need this method. It support modify the http request header
        """
        pass
