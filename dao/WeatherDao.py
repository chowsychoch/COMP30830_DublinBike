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
            'timezone': arr['timezone']
            # 'current':arr['current'],
            # 'hourly':arr['hourly'],
            # 'daily':arr['daily']
        }
    
    def filter_weather_action(self, weathers:list):
        # print('filer',weathers)
            weather = self.filter_Weather(weathers)
            print(weather)

    #TODO: create weather schema and insert scraped data.
    def insert_weather_to_db(self):

        pass
    