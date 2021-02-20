from sqlalchemy import Column, Integer, String, Float, DATETIME
from sqlalchemy.ext.declarative import declarative_base


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

