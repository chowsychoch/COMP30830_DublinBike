import requests
import json
import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class Weather_api:

    def __init__(self, api, appid):
        self._api = api
        self._appid = appid
        self._request = None
        # data type of station is a list of dictionary. e.g. [{},{},{}...]
        self.staions = []
        # self.lat = 53.3568
        # self.lon = -6.26814

    def sendRequest(self, lat, lon):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid,"lat": lat,"lon": lon})
            print(self._request.url)
            json.loads(self._request.text)
            self.staions.append(self._request.json())
        except:
            print("send request fail: ", self._request)

    # historical data use api_history.
    def sendRequest_h(self, lat, lon, dt):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "lat": lat, "lon": lon, "dt": dt})
            print(self._request.url)
            json.loads(self._request.text)
            self.staions.append(self._request.json())
        except:
            print("send request fail: ", self._request)
