import time
from models.BikeStations import Base
from utilities.dataScraping import JCD_api
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api
from dotenv import load_dotenv
import os

load_dotenv()

URI = os.getenv("URI")
PORT = "3306"
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
USER = os.getenv("User") # note: USER will get user name of this computer.

CONTRACT = "dublin"  # name of contract
API = os.getenv("API")  # and the JCDecaux endpoint
APIKEY = os.getenv("APIKEY")



if __name__ == '__main__':

    # new crawling Api
    # just keep one engine to use and pass to the BikeStation_api
    engine = create_engine("mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

    # create stations table in RDS
    Base.metadata.create_all(engine)

    # create dao obj
    dao = BikeStation_api(engine)

    # create JCD api obj
    jcd_obj = JCD_api(CONTRACT, API, APIKEY)


    # TODO: add some log record function.
    while True:
        try:
            # request JCD stations data
            jcd_obj.sendRequest()
            # insert rows into RDS
            dao.insert_stations_to_db(jcd_obj.staions)

            # pause for 5 min
            print("sleep for five min")
            time.sleep(5*60)
        except Exception as e:
            print("Error: Duplicate data!!!")
            time.sleep(1 * 60)
