import sqlalchemy as sqla
from sqlalchemy import Table, Column, Integer, String, Float, MetaData, DATETIME
from sqlalchemy import create_engine
import datetime

class sql_api:

    def __init__(self,USER, PASSWORD, URI, PORT, DB):
        self.engine = create_engine("mysql+mysqldb://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
        # print(self.engine.url)
        # connection = engine.connect()

    def create_schemas(self):

        pass

    def create_station_table(self):
        # create table
        meta = MetaData()
        stations = sqla.Table(
            'stations', meta,
            Column('number', Integer, primary_key= True),
            Column('name', String(128)),
            Column('address', String(128)),
            Column('pos_lat', Float),
            Column('pos_lng', Float),
            Column('bike_stands', Integer),
            Column('available_bike_stands', Integer),
            Column('available_bikes', Integer),
            Column('last_update', DATETIME, primary_key= True)
        )

        print(stations.columns)
        meta.create_all(self.engine)

    def filter_Station(self, arr):
        return {
                 'number': int(arr['number']),
                 'name': arr['name'],
                 'address': arr['address'],
                 'pos_lat': float(arr['position']['lat']),
                 'pos_lng': float(arr['position']['lng']),
                 'bike_stands': int(arr['bike_stands']),
                 'available_bike_stands': int(arr['available_bike_stands']),
                 'available_bikes': int(arr['available_bikes']),
                 'last_update': datetime.datetime.fromtimestamp(arr['last_update']/1e3)
        }

    def insert_stations_to_db(self, stations : list):

        # station : dictionary
        for station in stations:
            station = self.filter_Station(station)
            vals = (station["number"], station["name"], station["address"], station["pos_lat"], station["pos_lng"],
                    station["bike_stands"], station["available_bike_stands"], station["available_bikes"],
                    station["last_update"])
            print(vals)
            self.engine.execute("insert into stations value(%s,%s,%s,%s,%s,%s,%s,%s,%s)", vals)
            break

    #TODO:
    def select_data(self, ):

        pass

