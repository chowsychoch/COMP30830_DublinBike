from sqlalchemy import Column, Integer, String, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base

import sys
import os

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

Base = declarative_base()

'''create the model to save the data crawling from the Internet'''
class Weather(Base):
    __tablename__ = 'weather'
    number = Column('number', Integer, primary_key=True)
    lat = Column('lat', Float)
    lng = Column('lng', Float)
    timezone = Column('timezone', String(128))
    current = Column('current', DATETIME)
