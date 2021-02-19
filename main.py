import time

from COMP30830_DublinBike.utilities.dataScraping import JCD_api
from COMP30830_DublinBike.utilities.SQL_api import sql_api

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

    sql_obj = sql_api(USER, PASSWORD, URI, PORT, DB)
    sql_obj.create_station_table()

    jcd_obj = JCD_api(CONTRACT, API, APIKEY)

    while True:
        jcd_obj.sendRequest()
        sql_obj.insert_stations_to_db(jcd_obj.staions)
        time.sleep(5*60)


