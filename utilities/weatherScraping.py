import requests
import json
import sys
import os
import datetime
import pandas as pd

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

    # request forecast weather
    def sendRequest_forecast(self): #return dataframe
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "lat": 53.344, "lon": -6.2668, "exclude": "current,minutely,daily,alerts" })
            print(self._request.url)
            print(json.loads(self._request.text))
            # return 48 hours prediction from request time.
            self.staions = self._request.json()['hourly']
            return self.convert_list2df(self.staions)
        except:
            print("send request fail: ", self._request)

    def filter_Weather(self, arr: dict):

        return {
            'last_update': datetime.datetime.fromtimestamp(arr['dt']),
            'wind_speed': float(arr["wind_speed"]),
            'temperature': float(arr['temp']),
        }

    def convert_list2df(self, list_weather):
        weather_list = []
        for i in range(len(list_weather)):
            weather_list.append(self.filter_Weather(self.staions[i]))
        df = pd.DataFrame(weather_list)
        df['last_update'] = pd.to_datetime(df['last_update'])
        df = df.set_index('last_update')
        df['day_of_week'] = pd.to_datetime(df.index, format='%Y-%m-%d', errors='ignore').dayofweek
        df['time'] = [d.time() for d in df.index]
        # period = hour*6 + round(min/10)
        df['period'] = df.apply(lambda x: (int(round(x["time"].minute / 10)) + x["time"].hour * 6), axis=1)
        df = df[(df.period % 6 == 0) & (df.period != 0)]
        df['hour'] = df['period'] // 6
        df = df.reset_index()
        drop_column = ['time', 'period']
        df = df.drop(drop_column, axis=1)

        return df
