""" Module will ingest data into db using multiprocessing.
"""
import os
from datetime import datetime
import logging
import multiprocessing
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    Date,
    UniqueConstraint,
    String,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError


Base = declarative_base()


class WeatherData(Base):
    """
    Class to create a 'weather_data' table in the SQLite database using SQLAlchemy.

    Attributes:
    tablename (str): Name of the table in the database.
    id (Column): Column for the primary key of the table.
    date (Column): Column for the date of the weather data.
    maximum_temp (Column): Column for the maximum temperature of the weather data.
    minimum_temp (Column): Column for the minimum temperature of the weather data.
    precipitation (Column): Column for the precipitation of the weather data.
    station_id (Column): Column for the station id of the weather data.
    table_args (Tuple): Tuple to define the unique constraint for the table.
    """
    __tablename__ = "weather_data"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    maximum_temp = Column(Float)
    minimum_temp = Column(Float)
    precipitation = Column(Float)
    station_id = Column(String)
    __table_args__ = (
        UniqueConstraint("date", "maximum_temp", "minimum_temp", "precipitation"),
    )


def ingest_data(data_files):
    """
    Function to ingest data into the SQLite database from a given file.
    :param data_files: The file containing the data to be ingested.
    """
    try:
        start_time = datetime.now()
        engine = create_engine("sqlite:///code_assignment/src/weather.db")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        count = 0
        station_id = data_files.split(".")[0].split("/")[-1]
        print(f"processing file : {data_files}")
        logging.basicConfig(filename="weather_ingest.log", level=logging.INFO)
        with open(data_files, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("\t")
                date = parts[0]
                maximum_temp = float(parts[1])
                minimum_temp = float(parts[2])
                precipitation = float(parts[3])
                try:
                    date = datetime.strptime(parts[0], "%Y%m%d")
                    wd = WeatherData(
                        date=date,
                        maximum_temp=maximum_temp,
                        minimum_temp=minimum_temp,
                        precipitation=precipitation,
                        station_id=station_id,
                    )
                    session.add(wd)
                    session.commit()
                    count += 1
                except IntegrityError as err:
                    session.rollback()
                    logging.error(
                        """Duplicate data found for date: {},
                            maximum_temp: {},minimum_temp: {}, precipitation: {}""".format(
                            date, maximum_temp, minimum_temp, precipitation
                        )
                    )
        session.close()
        end_time = datetime.now()
        logging.info("Number of records ingested %s : %s", station_id, count)
        logging.info("Ingestion started at %s  and ended at %s", start_time, end_time)

    except RuntimeError as err:
        logging.info("Exception raised by following error %s", err)


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "code_assignment/wx_data")
    file_paths = [os.path.join(path, filename) for filename in os.listdir(path)]
    number_of_processes = multiprocessing.cpu_count()
    chunk_size = int(len(file_paths) / number_of_processes) + 1
    chunks = [
        file_paths[x : x + chunk_size] for x in range(0, len(file_paths), chunk_size)
    ]
    # Creating Multiporcess pool
    with multiprocessing.Pool() as pool:
        results = [pool.map(ingest_data, chunk) for chunk in chunks]
        pool.join()
        logging.info(
            "Number of records ingested: %s", sum(sum(result) for result in results)
        )
