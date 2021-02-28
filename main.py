import time
from models.BikeStations import Base
from models.Weather import Base
from utilities.dataScraping import JCD_api
from utilities.weatherScraping import Weather_api
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api
from dao.WeatherDao import weather_api
from dotenv import load_dotenv
import os

local_path = os.path.abspath(os.path.dirname(__file__))
config_path = local_path+"/.env"
load_dotenv(config_path)

URI = os.getenv("URI")
PORT = "3306"
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
USER = os.getenv("User") # note: USER will get user name of this computer.

CONTRACT = "dublin"  # name of contract
API = os.getenv("API")  # and the JCDecaux endpoint
APIKEY = os.getenv("APIKEY")
#weather api key
appid="ac8d0dd5f40c8d6da60fd0785a3f75c4"
api="https://api.openweathermap.org/data/2.5/onecall"

def main():
    # new crawling Api
    # just keep one engine to use and pass to the BikeStation_api
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

    # create stations table in RDS
    Base.metadata.create_all(engine)

    # create dao obj
    dao = BikeStation_api(engine)
    dao_weather = weather_api(engine)

    # create JCD api obj
    jcd_obj = JCD_api(CONTRACT, API, APIKEY)
    weather_api_obj = Weather_api(api, appid)

    # TODO: add some log record function.
    while True:
        try:
            # request JCD stations data
            jcd_obj.sendRequest()
            weather_api_obj.sendRequest()
            # insert rows into RDS
            dao.insert_stations_to_db(jcd_obj.staions)
            ## filter result for wather api 
            dao_weather.filter_weather_action(weather_api_obj.staions)
            # pause for 5 min
            print("sleep for five min")
            time.sleep(5 * 60)
        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)


if __name__ == '__main__':

    main()