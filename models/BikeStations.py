from sqlalchemy import Column, Integer, String, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Base = declarative_base()

'''create the model to save the data crawling from the Internet'''
class Stations(Base):
    __tablename__ = 'stations'
    number = Column('number', Integer, primary_key=True)
    name = Column('name', String(128))
    address = Column('address', String(128))
    pos_lat = Column('pos_lat', Float)
    pos_lng = Column('pos_lng', Float)
    bike_stands = Column('bike_stands', Integer)
    available_bike_stands = Column('available_bike_stands', Integer)
    available_bikes = Column('available_bikes', Integer)
    last_update = Column('last_update', DATETIME, primary_key=True)

    # reference: https://blog.csdn.net/u011089760/article/details/90142672
    def obj_to_dict(self):  # for build json format
        return {
            "number": self.number,
            "name": self.name,
            "address": self.address,
            "pos_lat": self.pos_lat,
            "pos_lng": self.pos_lng,
            "bike_stands": self.bike_stands,
            "available_bike_stands": self.available_bike_stands,
            "available_bikes": self.available_bikes,
            "last_update": str(self.last_update)
        }

