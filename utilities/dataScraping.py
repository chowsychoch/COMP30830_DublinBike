import requests
import json

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)


class JCD_api:

    def __init__(self, contract, api, apikey):
        self._contract = contract
        self._api = api
        self._apikey = apikey
        self._request = None
        # date type of stations is list of dictionary (json)
        self.staions = None
        # self.sendRequest()

    # sned request to JCD and store station data to self.stations
    # TODO: store another data
    def sendRequest(self):
        # TODO: add some error handling function
        try:
            # https://api.jcdecaux.com/vls/v1/stations?apiKey=45d8f343287c8759db0349d757fa9f77df198b71&contract=Dublin
            self._request = requests.get(self._api, params={"apiKey": self._apikey, "contract": self._contract})
            # print(self._request.url)
            json.loads(self._request.text)
            self.staions = self._request.json()
        except:
            print("send request fail: ", self._request)


