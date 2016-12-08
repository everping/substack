import json
from substack.plugins.base.port_plugin import PortPlugin
from bs4 import BeautifulSoup


class MxToolboxPlugin(PortPlugin):
    def __init__(self):
        PortPlugin.__init__(self)
        self.base_url = "http://mxtoolbox.com/Public/Lookup.aspx/DoLookup2"
        self.post_data = {"inputText": "scan:{host}", "resultIndex": 3}

    def setup_http(self):
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'X-NewRelic-ID': 'UwACUFBADQQEUFBR',
            'Content-Type': 'application/json; charset=utf-8',
            'MasterTempAuthorization': 'c74497f8-eccd-4c66-bd65-a4845206e28a',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://mxtoolbox.com/SuperTool.aspx?action=scan%3abkav.com&run=toolpage'
        }
        self.requester.set_header(headers)

    def real_scan(self, domain):

        payload = {"inputText": "scan:%s" % domain.ip, "resultIndex": 3}
        response = self.requester.post(self.base_url, data=json.dumps(payload)).text
        open_ports = self.extract(response)

        return open_ports

    def extract(self, response):
        response_json = json.loads(response)
        html_value = json.loads(response_json['d'])['HTML_Value']
        soup = BeautifulSoup(html_value, "lxml")

        tables = soup.findChildren('table')[0]
        rows = tables.find_all('tr')
        ports = []

        for row in rows:
            cell = row.find_all('td')
            try:
                if cell[3].string.lower() == "open":
                    ports.append(int(cell[1].string))
            except:
                pass
        return ports
