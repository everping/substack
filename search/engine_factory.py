from bing_engine import BingEngine
from baidu_engine import BaiduEngine


class EngineFactory():
    @staticmethod
    def create(engine_name):
        if engine_name == 'Bing':
            return BingEngine()
        elif engine_name == 'Baidu':
            return BaiduEngine()
