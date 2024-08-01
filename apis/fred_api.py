import requests
from urllib.parse import urlencode
from .base import BaseAPI
from config import FRED_API_KEY

class FREDAPI(BaseAPI):
    API_KEY = FRED_API_KEY
    BASE_URL = 'https://api.stlouisfed.org/fred/series/search'

    def fetch_data(self, search_text: str) -> dict:
        params = {
            'api_key': self.API_KEY,
            'search_text': search_text,
            'file_type': 'json',
            'search_type': 'full_text',
            'limit': 1000,
            'offset': 0,
            'order_by': 'search_rank',
            'sort_order': 'desc'
        }
        query_string = urlencode(params)
        url = f"{self.BASE_URL}?{query_string}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None

    def parse_response(self, response: dict, num_results=2) -> dict:
        parsed_data = []
        if 'seriess' in response:
            for series in response['seriess'][:num_results]:
                series_info = {
                    'id': series.get('id'),
                    'title': series.get('title'),
                    'frequency': series.get('frequency'),
                    'units': series.get('units'),
                    'observation_start': series.get('observation_start'),
                    'observation_end': series.get('observation_end'),
                    'popularity': series.get('popularity'),
                    'notes': series.get('notes')
                }
                parsed_data.append(series_info)
        return parsed_data

    def get_api_info(self) -> dict:
        return {
            "name": "FREDAPI",
            "description": "Fetches economic data series from the FRED API.",
            "base_url": self.BASE_URL
        }
