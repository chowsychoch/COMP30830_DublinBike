import time
from models.BikeStations import Base
from utilities.dataScraping import JCD_api
from utilities.SQL_api import sql_api
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api

URI = "dbike.cthcb1yq49ko.us-east-1.rds.amazonaws.com"
PORT = "3306"
PASSWORD ="ucd_s2_2021"
DB = "dbike"
USER = "root"

CONTRACT="Dublin" # name of contract
API="https://api.jcdecaux.com/vls/v1/stations" # and the JCDecaux endpoint
# API key should be hided
APIKEY = "45d8f343287c8759db0349d757fa9f77df198b71"


if __name__ == '__main__':

	# new crawling Api
	# just keep one engine to use and pass to the BikeStation_api
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)
    # create table
    Base.metadata.create_all(engine)
    dao = BikeStation_api(engine)
    jcd_obj = JCD_api(CONTRACT, API, APIKEY)
    # sql_obj = sql_api(USER, PASSWORD, URI, PORT, DB)
    # sql_obj.create_station_table()
    # jcd_obj = JCD_api(CONTRACT, API, APIKEY)

    while True:
        jcd_obj.sendRequest()
        dao.insert_stations_to_db(jcd_obj.staions)
        # sql_obj.insert_stations_to_db(jcd_obj.staions)
        time.sleep(5*60)


