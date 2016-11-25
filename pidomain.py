from search.engine_factory import EngineFactory

engines_name = ['Bing', 'Baidu']
engines = [EngineFactory.create(engine_name) for engine_name in engines_name]
domain = "bkav.com"
for engine in engines:
    print engine.get_name()
    print engine.discover(domain).__len__()
#
# class PiDomain:
#     def discover_worker(to_walk):
#         while len(to_walk)
