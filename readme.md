## API ENd points
> - for weather data : http://127.0.0.1:5000/api/weather
> - query for station and date : http://127.0.0.1:5000/api/weather?station_id=USC00257715&date=1985-01-01
> - for weather-stats : http://127.0.0.1:5000/api/weather/stats/
> - query for limit and pagination : http://127.0.0.1:5000/api/weather/stats?limit=10&page=3


## steps
> - For ceating weather.db in the sqlite db using orm please execute src/data_modular.py
> - For ceating weather.db and weather_data table in the sqlite db using ddl please execute src/data_modular_ddl.py
> - To injest the data into db execute the data_injection.py file.
> - To analyze the data please execute data_analysis.py file.
> - For API please execute data_api.py

## required modules.
Please Install the requirements.txt for required modules.

### test case execution and coverage.
> API should be running for test case execution.
python3 -m pytest --cov-report term-missing --cov=src

> used black for files formating and pylint for static code analysis.