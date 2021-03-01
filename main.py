from datetime import datetime
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
appid="ac8d0dd5f40c8d6da60fd0785a3f75c4"
api="https://api.openweathermap.org/data/2.5/onecall"
api_history = "https://api.openweathermap.org/data/2.5/onecall/timemachine"


class myThread (threading.Thread):
   def __init__(self, threadID,jcd_obj,weather_obj,dao_weather):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.jcd_obj = jcd_obj
        self.weather_obj = weather_obj
        self.dao_weather = dao_weather
   def run(self):
        print("Starting " + str(self.threadID))
        weather_api_run(self.jcd_obj,self.weather_obj,self.dao_weather)
        print("Exiting " + str(self.threadID))
        return

def weather_api_run(jcd_api_obj,weather_api_obj,dao_weather):

    for station in jcd_api_obj.staions:
        weather_api_obj.sendRequest_h(station["position"]['lat'], station["position"]['lng'], station['last_update'])
        time.sleep(0.2)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(weather_api_obj.staions, f, ensure_ascii=False, indent=4)

    weather_api_obj.staions = []

    ## filter result for wather api
    # dao_weather.filter_weather_action(weather_api_obj.staions)

    # TODO: Insert date to weather table.

    return


def main():
    # new crawling Api
    # just keep one engine to use and pass to the BikeStation_api
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

    # create stations table in RDS
    Base.metadata.create_all(engine)

    # create dao obj
    dao_bike = BikeStation_api(engine)
    dao_weather = weather_api(engine)

    # create JCD api obj
    jcd_api_obj = JCD_api(CONTRACT, API, APIKEY)
    weather_api_obj = Weather_api(api, appid)

    # TODO: add some log record function.
    while True:
        try:
            print("restart")
            # request JCD stations data
            jcd_api_obj.sendRequest()
            # using jcd_api_obj.staions to grep loation and time of each station as parameters of weather_api_obj.sendRequest()

            # create new thread to mapping bike station info with weather info.
            thread1 = myThread(1, jcd_api_obj, weather_api_obj, dao_weather)
            thread1.start()

            # insert rows into RDS
            dao_bike.insert_stations_to_db(jcd_api_obj.staions)
            # pause for 5 min
            print("sleep for five min")
            time.sleep(5 * 60)
        except Exception as e:
            print("something wrong", e)
            time.sleep(1 * 60)


if __name__ == '__main__':

    main()