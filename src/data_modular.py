""" This Script will create table in sqlite3 database.
"""
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class WeatherData(Base):
    """
    Model class to represent a weather record.

    Attributes:
        id (int): Unique identifier for the record.
        date (str): Date of the record.
        max_temp (float): Maximum temperature in degrees Celsius.
        min_temp (float): Minimum temperature in degrees Celsius.
        precipitation (float): Total accumulated precipitation in centimeters.
    """

    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    station_id = Column(String)
    maximum_temp = Column(Float)
    minimum_temp = Column(Float)
    precipitation = Column(Float)


def create_weather_table():
    """
    Function to create the 'weather' table in the SQLite database using SQLAlchemy.
    """
    engine = create_engine("sqlite:///code_assignment/src/weather.db")
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    # calling create_weather_table method to create table in db.
    create_weather_table()
