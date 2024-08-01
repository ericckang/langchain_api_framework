import requests
from .base import BaseAPI
from config import RIOT_API_KEY

class LeagueAPI(BaseAPI):
    BASE_URL = "https://na1.api.riotgames.com/lol/platform/v3/champion-rotations"
    API_KEY = RIOT_API_KEY

    def fetch_data(self) -> dict:
        url = f"{self.BASE_URL}?api_key={self.API_KEY}"
        response = requests.get(url)
        return response.json()

    def parse_response(self, response: dict) -> dict:
        if "freeChampionIds" in response and "freeChampionIdsForNewPlayers" in response:
            return {
                "max_new_player_level": response.get("maxNewPlayerLevel"),
                "free_champion_ids_for_new_players": response.get("freeChampionIdsForNewPlayers"),
                "free_champion_ids": response.get("freeChampionIds"),
            }
        else:
            return {"error": "Unexpected response structure or missing data"}

    def get_api_info(self) -> dict:
        return {
            "name": "LeagueAPI",
            "description": "Fetches champion rotations for League of Legends.",
            "base_url": self.BASE_URL
        }
