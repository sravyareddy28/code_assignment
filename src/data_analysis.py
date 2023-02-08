from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func, select

Base = declarative_base()


class WeatherData(Base):
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True)
    station_id = Column(Integer)
    date = Column(String)
    maximum_temp = Column(Float)
    minimum_temp = Column(Float)
    precipitation = Column(Float)


class WeatherStats(Base):
    """
    Class for creating a table weather_stats in a SQLite database.
    Attributes:
        weather_stats_id (int): Unique identifier for the record.
        station_id (string): Station id
        year (int): Date of the record.
        avg_maximum_temp (float): Average Maximum temperature in degrees Celsius.
        avg_minimum_temp (float): Average Minimum temperature in degrees Celsius.
        total_precipitation (float): Total accumulated precipitation in centimeters.
    """

    __tablename__ = "weather_stats"
    weather_stats_id = Column(Integer, primary_key=True)
    station_id = Column(Integer)
    year = Column(Integer)
    avg_maximum_temp = Column(Float)
    avg_minimum_temp = Column(Float)
    total_precipitation = Column(Float)


engine = create_engine("sqlite:///code_assignment/src/weather.db")
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def stats_calculation():
    """
    Method will calculate the avergae min and max tempuratures for all the stations.
    """
    try:
        conn = engine.connect()
        data = conn.execute(
            select(
                [
                    WeatherData.station_id,
                    func.strftime("%Y", WeatherData.date).label("year"),
                    func.avg(WeatherData.maximum_temp).label("avg_maximum_temp"),
                    func.avg(WeatherData.minimum_temp).label("avg_minimum_temp"),
                    func.sum(WeatherData.precipitation).label("total_precipitation"),
                ]
            )
            .select_from(WeatherData)
            .group_by(WeatherData.station_id, func.strftime("%Y", WeatherData.date))
        )

        results = data.fetchall()

        conn.execute(
            WeatherStats.__table__.insert(),
            [
                {
                    "station_id": record[0],
                    "year": record[1],
                    "avg_maximum_temp": record[2],
                    "avg_minimum_temp": record[3],
                    "total_precipitation": record[4],
                }
                for record in results
            ],
        )
        conn.close()

        # Commit the transaction
        session.commit()
    except Exception as err:
        print(f"Error occured due to {err}")


if __name__ == "__main__":
    # calling stats_calculatio method.
    stats_calculation()
