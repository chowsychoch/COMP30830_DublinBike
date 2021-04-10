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
        dict_stations[id] = df_stations.loc[df_stations['number'] == id][stations_feature_column].sort_values(
            'last_update')
        dict_stations[id] = dict_stations[id].dropna()
        dict_stations[id]['last_update'] = pd.to_datetime(dict_stations[id]['last_update'])
        dict_stations[id] = dict_stations[id].set_index('last_update')

        dict_stations[id]['available_bike_ratio'] = dict_stations[id]['available_bikes'] / dict_stations[id][
            'bike_stands']
        # day_of_week, 0 stands for Mon, 6 stands for Sat
        dict_stations[id]['day_of_week'] = pd.to_datetime(dict_stations[id].index, format='%Y-%m-%d',
                                                          errors='ignore').dayofweek
        dict_stations[id]['time'] = [d.time() for d in dict_stations[id].index]
        # period = hour*6 + round(min/10)
        dict_stations[id]['period'] = dict_stations[id].apply(
            lambda x: (int(round(x["time"].minute / 10)) + x["time"].hour * 6), axis=1)
        dict_stations[id] = merge_weather_bike(df_weather, dict_stations[id])
        dict_stations[id] = dict_stations[id][(dict_stations[id].period % 6 == 0) & (dict_stations[id].period != 0)]
        dict_stations[id]['hour'] = dict_stations[id]['period'] // 6
        dict_stations[id] = dict_stations[id].reset_index()

        dict_stations[id] = remove_outlier(dict_stations[id])
        dict_stations[id] = data_type_conversion(dict_stations[id])
        dict_stations[id] = dict_stations[id].dropna()
        dict_stations[id] = dict_stations[id].drop(drop_column, axis=1)
        dict_stations[id] = dict_stations[id].drop_duplicates().reset_index()
        dict_stations[id] = dict_stations[id].drop(['index'], axis=1)

    return dict_stations


'''load the model from disk'''
def make_prediction(df_weather, station_id):
    features = ['day_of_week', 'hour', 'wind_speed', 'temperature']

    filename = '../station_' + str(station_id) + '.sav'
    linreg = pickle.load(open(filename, 'rb'))

    # Print the estimated linear regression coefficients.
    print("Features: \n", features)
    print("Coeficients: \n", linreg.coef_)
    print("\nIntercept: \n", linreg.intercept_)

    linreg_predictions = linreg.predict(df_weather[features])

    return linreg_predictions

if __name__ == '__main__':
    '''Read csv file as dataframe'''
    df_weather = pd.read_csv('../weather.csv')
    del df_weather["Unnamed: 0"]

    df_stations = pd.read_csv('../stations.csv')
    del df_stations["Unnamed: 0"]

    df_weather = clean_weather_table(df_weather)
    dict_stations = separate_stations(df_stations, df_weather)

    df_weather = dict_stations[21].iloc[[20]]
    station_id = 36
    print(make_prediction(df_weather, station_id))

    # weather_api_obj = Weather_api(api_forecast, appid)
    #
    # weather_api_obj.sendRequest_forecast()
    # weather_api_obj.filter_Weather()

