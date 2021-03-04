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
        self.staions = None
        self.city = "Dublin"

    # historical data use api_history.
    def sendRequest(self, lat, lon, dt):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "lat": lat, "lon": lon, "dt": dt})
            print(self._request.url)
            json.loads(self._request.text)
            print(json.loads(self._request.text))
            self.staions.append(self._request.json())
        except:
            print("send request fail: ", self._request)

    # request city weather
    def sendRequest(self,id):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "id": id})
            print(self._request.url)
            print(json.loads(self._request.text))
            self.staions = self._request.json()
        except:
            print("send request fail: ", self._request)
