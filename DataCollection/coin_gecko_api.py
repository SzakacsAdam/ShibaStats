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

    def __genr_api_url(self, url: str, parameters: dict = None):
        api_url = f"{self.__API_URL_BASE}{url}"
        if parameters:
            api_url += '?'
            parms: list = [f"{key}={','.join(val)}" if isinstance(val, list)
                           else f"{key}={val}"
                           for key, val in parameters.items()]
            api_url += '&'.join(parms).lower()
        return api_url

    def ping(self) -> dict:
        """Check API server status"""
        url: str = "/ping"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_price(self, ids, vs_currencies, *, include_market_cap: bool = False,
                  include_24hr_vol: bool = False, include_24hr_change: bool = False,
                  include_last_updated_at: bool = False) -> dict:
        """Get the current price of any cryptocurrencies in any other supported 
        currencies that you need."""
        url: str = "/simple/price"
        parameters: dict = {"ids": ids, "vs_currencies": vs_currencies,
                            "include_market_cap": include_market_cap,
                            "include_24hr_vol": include_24hr_vol,
                            "include_24hr_change": include_24hr_change,
                            "include_last_updated_at": include_last_updated_at}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_token_price(self, id: str, contract_addresses, vs_currencies, *,
                        include_market_cap: bool = False,
                        include_24hr_vol: bool = False,
                        include_24hr_change: bool = False,
                        include_last_updated_at: bool = False) -> dict:
        """Get current price of tokens (using contract addresses) for a given 
           platform in any other currency that you need."""
        url: str = f"/simple/token_price/{id}"
        parameters: dict = {"contract_addresses": contract_addresses,
                            "vs_currencies": vs_currencies,
                            "include_market_cap": include_market_cap,
                            "include_24hr_vol": include_24hr_vol,
                            "include_24hr_change": include_24hr_change,
                            "include_last_updated_at": include_last_updated_at}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_supported_vs_currencies(self) -> list:
        """Get list of supported_vs_currencies."""
        url: str = "/simple/supported_vs_currencies"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_coins_list(self, *, include_platform: bool = False) -> list:
        """List all supported coins id, name and symbol (no pagination required)"""
        url: str = "/coins/list"
        parameters: dict = {"include_platform": include_platform}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)
    
    def get
