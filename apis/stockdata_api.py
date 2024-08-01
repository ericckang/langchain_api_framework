import requests
from .base import BaseAPI
from config import STOCKDATA_API_TOKEN

class StockAPI(BaseAPI):
    BASE_URL = "https://api.stockdata.org/v1/data/quote"
    NEWS_URL = "https://api.stockdata.org/v1/news/all"
    API_TOKEN = STOCKDATA_API_TOKEN

    def fetch_data(self, symbols: str) -> dict:
        url = f"{self.BASE_URL}?symbols={symbols}&api_token={self.API_TOKEN}"
        response = requests.get(url)
        return response.json()

    def parse_response(self, response: dict) -> dict:
        return response.get("data", {})

    def get_api_info(self) -> dict:
        return {
            "name": "StockAPI",
            "description": "Fetches stock data.",
            "base_url": self.BASE_URL
        }

    def fetch_news(self, symbols: str) -> dict:
        url = f"{self.NEWS_URL}?symbols={symbols}&api_token={self.API_TOKEN}"
        response = requests.get(url)
        return response.json()
