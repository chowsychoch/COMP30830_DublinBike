from sqlalchemy import Column, Integer, String, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Base_weather = declarative_base()

'''create the model to save the data crawling from the Internet'''
class Weather(Base_weather):
    __tablename__ = 'weather'
    lat = Column('lat', Float)
    lon = Column('lon', Float)
    timezone = Column('timezone', String(128))
    current = Column('current', DATETIME, primary_key=True)
    weather_id = Column('wether_id', Integer, primary_key=True)
    weather_icon = Column('weather_icon',String(10))
    visibility = Column('visibility', Float)
    wind_speed = Column('wind_speed', Float)
    wind_deg = Column('wind_deg', Float)
    wind_gust = Column('wind_gust', Float)
    temperature = Column('temperature', Float)
    feels_like = Column('feels_like', Float)
    temp_min = Column('temp_min', Float)
    temp_max = Column('temp_max', Float)
    pressure = Column('pressure', Float)
    humidity = Column('humidity', Float)
    rain_1h = Column('rain_1h', Float)
    snow_1h = Column('snow_1h', Float)
    sunrise = Column('sunrise', DATETIME)
    sunset = Column('sunset', DATETIME)
    description = Column('description', String(100))
