from abc import ABC, abstractmethod

class BaseAPI(ABC):
    @abstractmethod
    def fetch_data(self, query: str) -> dict:
        pass

    @abstractmethod
    def parse_response(self, response: dict) -> dict:
        pass

    @abstractmethod
    def get_api_info(self) -> dict:
        pass
