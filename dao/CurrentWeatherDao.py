import datetime
from sqlalchemy.orm import sessionmaker
from models.Weather import Base, Weather


class weather_api:
    #init method get engine from variable.
    def __init__(self,engine):
        self.engine = engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    # TODO: filter useful columns
    def filter_Weather(self, arr):
        # for item in current:
        #     'dt': datetime.datetime.fromtimestamp(arr['dt']/1e3),
        #     'sunrise': datetime.datetime.fromtimestamp(arr['sunrise']/1e3)
        for item in arr:
            if item == 'current':
                print(arr[item])
        return{
            # 'number': int(arr['number']),
            'lat': float(arr['lat']),
            'lon': float(arr['lon']),
            'timezone': arr['timezone'],
            'current' : datetime.datetime.fromtimestamp(arr['dt']/1e3),
            'weather_id' : int(arr['weather']['id']),
            'wind_speed' : float(arr['wind']['speed']),
            'temperature' : float(arr['main']['temp']),
            'description' : arr['weather']['main']
            # 'current':arr['current'],
            # 'hourly':arr['hourly'],
            # 'daily':arr['daily']
        }
    
    def filter_weather_action(self, weathers:list):
        # print('filer',weathers)
            weather = self.filter_Weather(weathers)
            print(weather)

    #TODO: create weather schema and insert scraped data.
    def insert_weather_to_db(self, weather : list):
        for weather_column in weather:
            try:
                weather_column = self.filter_Weather(weather_column)
                newWeather = Weather(
                lat = weather_column["lat"],
                lon = weather_column["lon"],
                timezone = weather_column["timezone"],
                current = weather_column["current"],
                weather_id = weather_column["weather_id"],
                wind_speed = weather_column["wind_speed"],
                temperature = weather_column["temperature"],
                description = weather_column["description"]
                )
                self.session.add(newWeather)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print('Error message', e)
                pass

