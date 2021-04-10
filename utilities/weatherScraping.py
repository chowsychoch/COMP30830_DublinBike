import requests
import json
import sys
import os
import datetime

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
    def sendRequest_forecast(self):
        try:
            self._request = requests.get(self._api, params={"appid": self._appid, "lat": 53.344, "lon": -6.2668, "exclude": ["current","minutely","daily","alerts"]})
            print(self._request.url)
            print(json.loads(self._request.text))
            self.staions = self._request.json()
        except:
            print("send request fail: ", self._request)

    def filter_Weather(self, arr: dict):
        if 'gust' not in arr['wind']:
            d_gust = 0
        else:
            d_gust = arr['wind']['gust']
        if 'rain' not in arr:
            d_rain = 0
        else:
            d_rain = arr['rain']['rain_1h']
        if 'snow' not in arr:
            d_snow = 0
        else:
            d_snow = arr['snow']['snow_1h']
        return {
            'lat': float(arr["coord"]['lat']),
            'lon': float(arr["coord"]['lon']),
            'timezone': arr['timezone'],
            'current': datetime.datetime.fromtimestamp(arr['dt']),
            'weather_id': int(arr['weather'][0]['id']),
            'weather_icon': arr['weather'][0]['icon'],
            'visibility': arr['visibility'],
            'wind_speed': float(arr['wind']['speed']),
            'wind_deg': float(arr['wind']['deg']),
            'wind_gust': float(d_gust),
            'temperature': float(arr['main']['temp']),
            'feels_like': float(arr['main']['feels_like']),
            'temp_min': float(arr['main']['temp_min']),
            'temp_max': float(arr['main']['temp_max']),
            'pressure': float(arr['main']['pressure']),
            'humidity': float(arr['main']['humidity']),
            'rain_1h': float(d_rain),
            'snow_1h': float(d_snow),
            'sunrise': datetime.datetime.fromtimestamp(arr['sys']['sunrise']),
            'sunset': datetime.datetime.fromtimestamp(arr['sys']['sunset']),
            'description': arr['weather'][0]['main']
        }
