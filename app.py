# Basic usage
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Data processing
import pandas as pd

# Customized usage
from dao.BikeStationsDao import BikeStation_api
from dao.CurrentWeatherDao import weather_api
from models.BikeStations import Stations

# Web development
from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from jinja2 import Template


local_path = os.path.abspath(os.curdir)
print(local_path)
config_path = local_path+"/.env"
print(config_path)
load_dotenv(config_path)
URI = os.getenv("URI")
PORT = "3306"
PASSWORD = os.getenv("PASSWORD")
DB = os.getenv("DB")
USER = os.getenv("User") # note: USER will get user name of this computer.
mysql_url = "mysql+pymysql://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB)

#____________________________________________________________________________________#

app = Flask(__name__)

engine = create_engine(mysql_url, echo=True)
dao_bike = BikeStation_api(engine)

# reference: https://blog.csdn.net/u011089760/article/details/90142672
def dict_helper(objlist):
    result = [item.obj_to_dict() for item in objlist]
    return result

##The result return is not always the whole stations point***
@app.route("/stations")
def get_stations():
    data = []
    # query the station with more than 10 avalible bike within 10 minutes from current time.
    now_minus_10 = (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
    stations_info = dao_bike.session.query(Stations).filter(Stations.last_update > now_minus_10).filter(
        Stations.available_bikes > 0).all()
    stations_list_dict = dict_helper(stations_info)

    return jsonify(stations=stations_list_dict)

#Get the all station points with their latest update
@app.route("/station")
def get_station():
    df = pd.read_sql_query("select number,name, address,pos_lat,pos_lng,bike_stands,available_bikes,max(last_update) from dublinBike.stations group by number",engine)
    print(df.head().to_json(orient='records'))
    return df.to_json(orient='records')

@app.route("/test")
def test():
    #TODO: connect with stations.html
    pass
@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(debug=True)