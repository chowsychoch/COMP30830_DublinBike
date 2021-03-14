from flask import Flask, render_template, request, jsonify

from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from dao.BikeStationsDao import BikeStation_api
from dao.CurrentWeatherDao import weather_api
from models.BikeStations import Stations
import pandas as pd



local_path = os.path.abspath(os.curdir)+"/.."
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

app = Flask(__name__)

engine = create_engine(mysql_url, echo=True)
dao_bike = BikeStation_api(engine)


# @app.route('/')
# def index():
#     # query the station with more than 10 avalible bike within 10 minutes from current time.
#     now_minus_10 = (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
#     print(now_minus_10)
#     station_info = dao_bike.session.query(Stations).filter(Stations.last_update > now_minus_10).filter(
#         Stations.available_bikes > 10).all()
#     return str(len(station_info))

@app.route("/")
def index():
    return app.send_static_file("index.html")

##The result return is not always the whole stations point***
@app.route("/stations")
def get_stations():
    data = []
    # query the station with more than 10 avalible bike within 10 minutes from current time.
    now_minus_10 = (datetime.now() - timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")

    stations_info = dao_bike.session.query(Stations).filter(Stations.last_update > now_minus_10).filter(
        Stations.available_bikes > 10).all()
    for row in stations_info: # TODO: issue Object of type Stations is not JSON serializable.
        data.append(dict(row))

    return jsonify(stations=stations_info)

#Get the all station points with their latest update
@app.route("/station")
def get_station():
    df = pd.read_sql_query("select number,name, address,pos_lat,pos_lng,bike_stands,available_bikes,max(last_update) from dublinBike.stations group by number",engine)
    print(df.head().to_json(orient='records'))
    return df.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)