import datetime
from sqlalchemy.orm import sessionmaker
from models.BikeStations import Base, Stations


class BikeStation_api:

    # init method get the engine from the variable, so that can access the database together
    def __init__(self,engine):
        self.engine = engine
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    '''
    get the data mapping to the table of database and 
    use a function filter some data. we don't need all the data from json
    '''
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

    '''
    This is insert the data to table. use model to mapping the column of database table
    '''
    def insert_stations_to_db(self, stations: list):
        # station : dictionary
        # try: 
        for station in stations:
            try:
                station = self.filter_Station(station)
                newSta = Stations(number = station["number"],
                              name = station["name"],
                              address = station["address"],
                              pos_lat = station["pos_lat"],
                              pos_lng = station["pos_lng"],
                              bike_stands = station["bike_stands"],
                              available_bike_stands = station["available_bike_stands"],
                              available_bikes = station["available_bikes"],
                              last_update = station["last_update"])
                self.session.add(newSta)
                self.session.commit()
            except Exception as e:
                self.session.rollback()
                print('Error message',e)
                pass
        # except Exception as e:
        #     print("sss", e)

    #TODO:
    def select_data(self, ):

        pass

    #TODO:
    def create_schemas(self):

        pass
