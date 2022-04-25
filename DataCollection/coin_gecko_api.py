from requests import Session

class CoinGeckoAPI:
    __API_URL_BASE: str = "https://api.coingecko.com/api/v3"

    def __init__(self, api_base_url: str = __API_URL_BASE) -> None:
        self.api_base_url = api_base_url
        self.session = Session()
        self.timeout: int = 60
    