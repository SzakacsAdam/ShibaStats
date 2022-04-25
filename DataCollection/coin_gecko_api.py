from requests import Session
from json import loads
from requests.exceptions import HTTPError
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from requests.exceptions import RequestException


class CoinGeckoAPI:
    __API_URL_BASE: str = "https://api.coingecko.com/api/v3"

    def __init__(self, api_base_url: str = __API_URL_BASE) -> None:
        self.api_base_url = api_base_url
        self.session = Session()
        self.timeout: int = 60

    def __request(self, url) -> str:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
        except HTTPError:
            raise
        except ConnectionError:
            raise
        except Timeout:
            raise
        except RequestException:
            raise

        else:
            return loads(response.content.decode('utf-8'))
