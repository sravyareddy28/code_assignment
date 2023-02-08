""" API End points for weather and weather stats data.
"""
import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./weather.db"
db = SQLAlchemy(app)

# pylint: disable=no-member
class WeatherData(db.Model):
    """Class for WeatherStats schema
    """
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    date = db.Column(db.String)
    maximum_temp = db.Column(db.Float)
    minimum_temp = db.Column(db.Float)
    precipitation = db.Column(db.Float)

# pylint: disable=no-member
class WeatherStats(db.Model):
    """Class for WeatherStats schema
    """
    weather_stats_id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String)
    year = db.Column(db.Integer)
    avg_maximum_temp = db.Column(db.Float)
    avg_minimum_temp = db.Column(db.Float)
    total_precipitation = db.Column(db.Float)


@app.route("/api/weather", methods=["GET"])
def weather():
    """end point for weather data
      returns : JSON-formatted response.
    """
    limit = int(request.args.get("limit", 10))
    station_id = request.args.get("station_id", None)
    date = request.args.get("date", None)
    page = int(request.args.get("page", 1))

    weather_data = WeatherData.query

    if station_id:
        weather_data = weather_data.filter_by(station_id=station_id)
    if date:
        weather_data = weather_data.filter_by(date=date)

    total_records = weather_data.count()
    total_pages = (total_records + limit - 1) // limit

    weather_data = weather_data.offset((page - 1) * limit).limit(limit)

    data = [
        {
            "id": wd.id,
            "station_id": wd.station_id,
            "date": wd.date,
            "maximum_temp": wd.maximum_temp,
            "minimum_temp": wd.minimum_temp,
            "precipitation": wd.precipitation,
        }
        for wd in weather_data
    ]

    return json.dumps(
        {"data": data, "total_records": total_records, "total_pages": total_pages}
    )


@app.route("/api/weather/stats", methods=["GET"])
def weather_stats_():
    """end point for weather-stats data
       returns : JSON-formatted response.
    """
    limit = int(request.args.get("limit", 10))
    station_id = request.args.get("station_id", None)
    year = request.args.get("year", None)
    page = int(request.args.get("page", 1))

    weather_stats = WeatherStats.query

    if station_id:
        weather_stats = weather_stats.filter_by(station_id=station_id)
    if year:
        weather_stats = weather_stats.filter_by(year=year)

    total_records = weather_stats.count()
    total_pages = (total_records + limit - 1) // limit

    weather_stats = weather_stats.offset((page - 1) * limit).limit(limit)

    data = [
        {
            "id": ws.weather_stats_id,
            "station_id": ws.station_id,
            "date": ws.year,
            "avg_maximum_temp": ws.avg_maximum_temp,
            "avg_minimum_temp": ws.avg_minimum_temp,
            "total_precipitation": ws.total_precipitation,
        }
        for ws in weather_stats
    ]

    return json.dumps(
        {"data": data, "total_records": total_records, "total_pages": total_pages}
    )


if __name__ == "__main__":
    app.run(debug=True)
