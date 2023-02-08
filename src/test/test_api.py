import unittest
import requests
import json


class TestWeatherAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://127.0.0.1:5000"

    def test_weather(self):
        response = requests.get(f"{self.base_url}/api/weather")
        data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("total_records", data)
        self.assertIn("total_pages", data)

    def test_weather_stats(self):
        response = requests.get(f"{self.base_url}/api/weather/stats")
        data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("total_records", data)
        self.assertIn("total_pages", data)

    def test_weather_filters(self):
        response = requests.get(
            f"{self.base_url}/api/weather?limit=2&station_id=station_1&date=2022-01-01&page=1"
        )
        data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("total_records", data)
        self.assertIn("total_pages", data)

    def test_weather_stats_filters(self):
        response = requests.get(
            f"{self.base_url}/api/weather/stats?limit=2&station_id=station_1&year=2022&page=1"
        )
        data = json.loads(response.text)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", data)
        self.assertIn("total_records", data)
        self.assertIn("total_pages", data)


if __name__ == "__main__":
    unittest.main()
