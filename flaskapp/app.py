# Basic usage
import os,sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Data processing
import pandas as pd
import json
print (sys.path)
#vscode usage
sys.path.append(os.path.abspath(os.curdir))

# Customized usage
from dao.BikeStationsDao import BikeStation_api
from dao.CurrentWeatherDao import weather_api
from models.BikeStations import Stations
from flaskapp.daily_prediction import return_predict
# Web development
from flask_fontawesome import FontAwesome

from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
# from jinja2 import Template,PackageLoader, Environment
#Pycharm usage 
#local_path = os.path.abspath(os.curdir)+"/.."
#vs code usage 
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
fa = FontAwesome(app)
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
    stations_info = dao_bike.session.query(Stations).distinct(Stations.name).filter(Stations.last_update > now_minus_10).filter(
        Stations.available_bikes > 0).order_by(Stations.name).all() #TODO: Issue duplicate station name.
    stations_list_dict = dict_helper(stations_info)
    return render_template('stations.html', stations_info=stations_list_dict)
    # return jsonify(stations=stations_list_dict)


#Get the all station points with their latest update
@app.route("/station")
def get_station():
    df = pd.read_sql_query("select number,name, address,pos_lat,pos_lng,bike_stands,available_bikes,max(last_update) from dublinBike.stations group by number",engine)
    print(df.head().to_json(orient='records'))
    return df.to_json(orient='records')

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stations/<int:station_id>")
def station_msg(station_id):
    sql = f"""
    select name, address, available_bike_stands, available_bikes from stations where number = {station_id} order by last_update desc limit 1
    """
    df = pd.read_sql_query(sql, engine)
    return df.to_json(orient='records')

@app.route("/weather_forecast")
def weather_forecast():
    pass

@app.route("/occupancy/<int:station_id>")
def get_occupancy(station_id):
    sql = f"""
    select number, name, available_bikes, WEEKDAY(last_update) as Weekday, last_update from stations where number = {station_id}
    """
    df = pd.read_sql_query(sql, engine)
    name = df['name'].values[0]
    res_df = df.set_index('last_update').resample('1d').mean()
    res_df['last_update'] = res_df.index
    res_df['name'] = name
    return res_df.to_json(orient='records')

@app.route("/about")
def get_about():
    return render_template('about.html')
    
@app.route("/predict/<int:station_id>")
def predict_daily(station_id):
    predict_linear = return_predict(station_id)
    # get the data of weekday
    toJson = json.dumps(predict_linear)
    return toJson

if __name__ == "__main__":
    app.run(debug=True)
