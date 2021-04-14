# Basic usage
import os,sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Data processing
import pandas as pd
from pandas import to_datetime
import numpy as np
import csv
import pickle

print (sys.path)
#vscode usage
sys.path.append(os.path.abspath(os.curdir))

# Customized usage
from utilities.weatherScraping import Weather_api



#Pycharm usage
#local_path = os.path.abspath(os.curdir)+"/.."
#vs code usage
local_path = os.path.abspath(os.curdir)
print(local_path)

local_path = os.path.abspath(os.path.dirname(__file__))
config_path = local_path+"/../.env"
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
api_forecast =os.getenv("API_FCAST")

'''Clean weather data'''
def clean_weather_table(df):
    feature_column = ["current", "feels_like", "humidity", "wind_speed", "wether_id"]
    # df_weather = df[feature_column]
    df = df.rename(columns={'current': 'last_update'})
    df = df.sort_values('last_update')
    df['last_update'] = pd.to_datetime(df['last_update'])
    df = df.set_index('last_update')
    df = df.dropna()

    return df

'''Merge weather and bike table by last_update column'''
def merge_weather_bike(df_weather, df_station):
    tol = pd.Timedelta('5 minute')
    df_merge = pd.merge_asof(left=df_weather, right=df_station, right_index=True, left_index=True, direction='nearest',
                             tolerance=tol)
    return df_merge

'''Convert data type'''
def data_type_conversion(df):
    df['period'] = df['period'].astype('int64')
    df['hour'] = df['hour'].astype('int64')
    df['day_of_week'] = df['day_of_week'].astype('int64')

    return df

'''Remove outlier before training'''
def remove_outlier(df):
    df = df[np.abs(df["available_bike_ratio"]-df["available_bike_ratio"].mean())<=(3*df["available_bike_ratio"].std())]
    return df

'''Separate stations to specific station and drop redundant columns'''
def separate_stations(df_stations, df_weather):
    stations_id = df_stations["number"].unique()
    stations_feature_column = ["last_update", "number", "bike_stands", "available_bikes"]
    drop_column = ['timezone', 'lat', 'lon', 'description', 'time', 'period', 'rain_1h', 'snow_1h']
    dict_stations = {}

    for id in stations_id:
        df = df_stations.loc[df_stations['number'] == id][stations_feature_column].sort_values(
            'last_update')
        df = df.dropna()
        df['last_update'] = pd.to_datetime(df['last_update'])
        df = df.set_index('last_update')

        df['available_bike_ratio'] = df['available_bikes'] / df[
            'bike_stands']
        # day_of_week, 0 stands for Mon, 6 stands for Sat
        df['day_of_week'] = pd.to_datetime(df.index, format='%Y-%m-%d',
                                                          errors='ignore').dayofweek
        df['time'] = [d.time() for d in df.index]
        # period = hour*6 + round(min/10)
        df['period'] = df.apply(
            lambda x: (int(round(x["time"].minute / 10)) + x["time"].hour * 6), axis=1)
        df = merge_weather_bike(df_weather, df)
        df = df[(df.period % 6 == 0) & (df.period != 0)]
        df['hour'] = df['period'] // 6
        df = df.reset_index()

        df = remove_outlier(df)
        df = data_type_conversion(df)
        df = df.dropna()
        df = df.drop(drop_column, axis=1)
        df = df.drop_duplicates().reset_index()
        df = df.drop(['index'], axis=1)

    return dict_stations


'''load the model from disk'''
def make_prediction(df_weather,station_id,stands = 40):

    dict_weekDay = {0:"Mon",1:"Tue",2:"Wed",3:"Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    features = ['day_of_week', 'hour', 'wind_speed', 'temperature']
    # filename = '../station_' + str(station_id) + '.sav'
    # filename = './station_' + str(station_id) + '.sav'

    local_path = os.path.abspath(os.curdir)
    filename = local_path + '/station_' + str(station_id) + '.sav'
    linreg = pickle.load(open(filename, 'rb'))

    # Print the estimated linear regression coefficients.
    print("Features: \n", features)
    print("Coeficients: \n", linreg.coef_)
    print("\nIntercept: \n", linreg.intercept_)

    weekday = df_weather.day_of_week.unique()
    res_dict ={
            "station_id": station_id,
            "weekOfDay":{
            #     "Mon": {"hour": {1 : {"ava_bikes": ava_bikes,"ava_stands": ava_stands}, 2 : {"ava_bikes": ava_bikes,"ava_stands": ava_stands}},
            #     "Tue": {"hour": {}},
            #     "Wed": {"hour": {}},
            #     "Thu": {"hour": {}},
            #     "Fri": {"hour": {}},
            #     "Sat": {"hour": {}},
            #     "Sun": {"hour": {}}
                }
            }

    for day in weekday:
        res_dict["weekOfDay"][dict_weekDay[day]] = {"hour":{}}

    linreg_predictions = linreg.predict(df_weather[features])

    ''''{"station_id": station_id, "weekOfDay" : {"Mon" : {"hour": {1 : {"ava_bikes": ava_bikes,"ava_stands": ava_stands}, 2:{"wind_speed": wind_speed,"temperature": temperature} }},"Tue" : {"hour": {1 : {"wind_speed": wind_speed,"temperature": temperature}, 2:{"wind_speed": wind_speed,"temperature": temperature} }} }}'''
    for i in range(len(df_weather["hour"])-24): # only shows one day forecast
        weekday = dict_weekDay[df_weather["day_of_week"][i]]
        hour = str(df_weather["hour"][i])
        ava_bike = int(linreg_predictions[i]*stands)
        ava_stands = stands - int(linreg_predictions[i]*stands)
        res_dict["weekOfDay"][weekday]["hour"][hour] = {"ava_bikes": ava_bike,"ava_stands": ava_stands}
    return res_dict

def return_predict(station_id):

    weather_api_obj = Weather_api(api_forecast, appid)

    df_weather = weather_api_obj.sendRequest_forecast()

    return make_prediction(df_weather, station_id)

# if __name__ == '__main__':
#
#     weather_api_obj = Weather_api(api_forecast, appid)
#
#     df_weather = weather_api_obj.sendRequest_forecast()
#
#     station_id = 36
#
#     print(make_prediction(df_weather, station_id))

