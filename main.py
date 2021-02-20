import time
from models.BikeStations import Base
from utilities.dataScraping import JCD_api
from utilities.SQL_api import sql_api
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api
from dotenv import load_dotenv
import os
load_dotenv()

URI = os.getenv("URI")
PORT = "3306"
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
USER = os.getenv("User")

CONTRACT = "dublin"  # name of contract
API = os.getenv("API")  # and the JCDecaux endpoint
# API key should be hided
APIKEY = os.getenv("APIKEY")


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
