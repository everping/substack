from substack.plugins.port.mxtoolbox_engine import MxToolboxEngine
from substack.data.domain import Domain

#
d = Domain('ca.bkav.com')
m = MxToolboxEngine()
m.scan(d)
