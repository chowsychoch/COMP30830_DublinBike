from datetime import datetime
import time
from models.BikeStations import Base
from models.CurrentWeather import Base_weather # bug fix: rename base.
from utilities.dataScraping import JCD_api
from utilities.weatherScraping import Weather_api
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api
from dao.CurrentWeatherDao import weather_api
from dotenv import load_dotenv
import os
import json
import threading



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
appid=os.getenv("APIKEY_W")
api= os.getenv("API_W")
api_history = os.getenv("API_W")
api_city =os.getenv("API_W_CITY")


class myThread (threading.Thread):
   def __init__(self, threadID,jcd_obj,dao_bike):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.jcd_obj = jcd_obj
        self.dao_bike = dao_bike
   def run(self):
        print("Starting " + str(self.threadID))
        station_api_run(self.jcd_obj,self.dao_bike)
        print("Exiting " + str(self.threadID))
        return

def weather_api_history_run(jcd_api_obj,weather_api_obj,dao_weather):

    for station in jcd_api_obj.staions:
        weather_api_obj.sendRequest(station["position"]['lat'], station["position"]['lng'], station['last_update'])

    # just for view the data
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(weather_api_obj.staions, f, ensure_ascii=False, indent=4)

    ## filter result for wather api
    # dao_weather.filter_weather_action(weather_api_obj.staions)

    # TODO: Insert date to weather table.

    # clear stations cause it use append to add new list.
    weather_api_obj.staions = []
    return


def weather_api_city_run(weather_api_obj, dao_weather):
    # Dublin city code : 2964574
    weather_api_obj.sendRequest(2964574)
    # insert rows into RDS
    dao_weather.insert_weather_to_db_forSingleDict(weather_api_obj.staions)

def station_api_run(jcd_api_obj,dao_bike):
    # request JCD stations data
    jcd_api_obj.sendRequest()
    # insert rows into RDS
    dao_bike.insert_stations_to_db(jcd_api_obj.staions)

def main():
    # new crawling Api
    # just keep one engine to use and pass to the BikeStation_api
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

    # create stations table in RDS
    Base.metadata.create_all(engine)
    # create weather table in RDS
    Base_weather.metadata.create_all(engine)

    # create dao obj
    dao_bike = BikeStation_api(engine)
    dao_weather = weather_api(engine)

    # create JCD api obj
    jcd_api_obj = JCD_api(CONTRACT, API, APIKEY)
    weather_api_obj = Weather_api(api_city, appid)

    # TODO: add some log record function.
    while True:
        try:
            print("restart")
            # request JCD stations data
            weather_api_city_run(weather_api_obj,dao_weather)

            # create new thread to scarp bike station info .
            thread1 = myThread(1, jcd_api_obj,dao_bike)
            thread1.start()

            # pause for 10 min
            print("sleep for ten min")
            time.sleep(10 * 60)

        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)


if __name__ == '__main__':

    main()