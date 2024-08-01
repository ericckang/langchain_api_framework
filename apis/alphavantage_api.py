import requests
from config import ALPHA_VANTAGE_API_KEY
from .base import BaseAPI

class AlphaVantageAPI(BaseAPI):
    BASE_URL = "https://www.alphavantage.co/query"
    api_key = ALPHA_VANTAGE_API_KEY
    
    def fetch_data(self, symbols: str) -> dict:
        function = "GLOBAL_QUOTE"
        symbol = symbols.split(',')[0]
        url = f"{self.BASE_URL}?function={function}&symbol={symbol}&apikey={self.api_key}"
        response = requests.get(url)
        return response.json()

    def parse_response(self, response: dict) -> dict:
        return response.get("data", {})

    def get_api_info(self) -> dict:
        return {
            "name": "AlphaVantageAPI",
            "description": "Fetches stock data and financial news from Alpha Vantage.",
            "base_url": self.BASE_URL
        }

    def fetch_news(self, symbols: str, topics=None, time_from=None, time_to=None, sort='LATEST', limit=50) -> dict:
        function = "NEWS_SENTIMENT"
        tickers = ','.join(symbols.split(','))
        url = f"{self.BASE_URL}?function={function}&apikey={self.api_key}"
        
        # Constructing query parameters
        if tickers:
            url += f"&tickers={tickers}"
        if topics:
            url += f"&topics={','.join(topics)}"
        if time_from:
            url += f"&time_from={time_from}"
        if time_to:
            url += f"&time_to={time_to}"
        if sort:
            url += f"&sort={sort}"
        if limit:
            url += f"&limit={limit}"
        
        response = requests.get(url)
        return response.json()
