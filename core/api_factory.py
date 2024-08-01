from apis.stockdata_api import StockAPI
from apis.fred_api import FREDAPI
from apis.alphavantage_api import AlphaVantageAPI
from apis.league_api import LeagueAPI
from apis.brawlstars_api import BrawlStarsAPI
from apis.mealdb_api import MealDBAPI

class APIFactory:
    @staticmethod
    def get_api(api_type):
        if api_type == 'stock':
            return AlphaVantageAPI
        elif api_type == 'fred':
            return FREDAPI
        elif api_type == 'league':
            return LeagueAPI
        elif api_type == 'brawlstars':
            return BrawlStarsAPI
        elif api_type == 'meal':
            return MealDBAPI
        else:
            raise ValueError(f"Unknown API type: {api_type}")
