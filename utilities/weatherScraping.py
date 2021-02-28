import requests
import json

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Weather_api:

    def __init__(self,api,appid):
        self._api = api
        self._appid = appid
        self._request = None
        self.staions = None
        self.lat = 53.3568
        self.lon = -6.26814

    def sendRequest(self):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid,"lat":self.lat,"lon":self.lon})
            # print(self._request.url)
            json.loads(self._request.text)
            self.staions = self._request.json()
            # print(self.staions)
        except:
            print("send request fail: ", self._request)


