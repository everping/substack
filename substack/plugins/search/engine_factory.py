from substack.plugins.search.bing_engine import BingEngine
from substack.plugins.search.baidu_engine import BaiduEngine


class EngineFactory():
    def __init__(self):
        pass



    @staticmethod
    def create(engine_name, requester=None):
        engine = None

        if engine_name == 'BingEngine':
            engine = BingEngine()

        elif engine_name == 'BaiduEngine':
            engine = BaiduEngine()

        engine.set_requester(requester)

        return engine
