import datetime
from sqlalchemy.orm import sessionmaker
from models.CurrentWeather import Base_weather, Weather


class weather_api:
    # init method get engine from variable.
    def __init__(self, engine):
        self.engine = engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    # TODO: filter useful column
    def __filter_Weather_v2(self, arr: dict):
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

        return{
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

    def insert_weather_to_db_forSingleDict(self, weather: dict):
        try:
            weather_column = self.__filter_Weather_v2(weather)
            print('here',weather_column["wind_gust"])
            newWeather = Weather(
                lat=weather_column["lat"],
                lon=weather_column["lon"],
                timezone=weather_column["timezone"],
                current=weather_column["current"],
                weather_id=weather_column["weather_id"],
                weather_icon=weather_column["weather_icon"],
                visibility=weather_column["visibility"],
                wind_speed=weather_column["wind_speed"],
                wind_deg=weather_column["wind_deg"],
                wind_gust=weather_column["wind_gust"],
                temperature=weather_column["temperature"],
                feels_like=weather_column["feels_like"],
                temp_min=weather_column["temp_min"],
                temp_max=weather_column["temp_max"],
                pressure=weather_column["pressure"],
                humidity=weather_column["humidity"],
                rain_1h=weather_column["rain_1h"],
                snow_1h=weather_column["snow_1h"],
                sunrise=weather_column["sunrise"],
                sunset=weather_column["sunset"],
                description=weather_column["description"]
            )
            self.session.add(newWeather)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print('Error message', e)
            pass
