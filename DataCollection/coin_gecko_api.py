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
                           if val else ''
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

    def get_coins(self):
        url: str = "/coins"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_coins_list(self, *, include_platform: bool = False) -> list:
        """List all supported coins id, name and symbol (no pagination required)"""
        url: str = "/coins/list"
        parameters: dict = {"include_platform": include_platform}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coins_markets(self, vs_currency, *, ids='', category='',
                          order: str = 'market_cap_desc', per_page: int = 100,
                          page: int = 1, sparkline: bool = False,
                          price_change_percentage='') -> list:
        """List all supported coins price, market cap, volume, 
           and market related data."""
        url: str = "/coins/markets"
        parameters: dict = {"vs_currency": vs_currency, "ids": ids,
                            "category": category, "order": order,
                            "per_page": per_page, "page": page, "sparkline": sparkline,
                            "price_change_percentage": price_change_percentage}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_by_id(self, id: str, *, localization: bool = True, tickers: bool = True,
                       market_data: bool = True, community_data: bool = True,
                       developer_data: bool = True, sparkline: bool = True) -> dict:
        """Get current data (name, price, market, ... including exchange tickers) 
           for a coin"""
        url: str = f"/coins/{id}"
        parameters: dict = {"localization": localization, "tickers": tickers,
                            "market_data": market_data, "community_data": community_data,
                            "developer_data": developer_data, "sparkline": sparkline}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_by_id_tickers(self, id: str, *, exchange_ids='', include_exchange_logo='',
                               page: int = 1, order: str = "trust_score_asc",
                               depth: bool = False) -> dict:
        """Get coin tickers (paginated to 100 items)"""
        url: str = f"/coins/{id}/tickers"
        parameters: dict = {"exchange_ids": exchange_ids,
                            "include_exchange_logo": include_exchange_logo,
                            "page": page, "order": order,
                            "depth": depth}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_history(self, id: str, date: str = "01-01-2022", *,
                         localization=False) -> dict:
        """Get historical data (name, price, market, stats) at a given date for a coin"""
        url: str = f"/coins/{id}/history"
        parameters: dict = {"date": date, "localization": localization}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_market_chart(self, id: str, vs_currency, days='max', *,
                              interval: str = "daily") -> dict:
        """Get historical market data include price, market cap, and 24h volume (granularity auto)"""
        url: str = f"/coins/{id}/market_chart"
        parameters: dict = {"vs_currency": vs_currency, "days": days,
                            "interval": interval}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_market_chart_range(self, id: str, vs_currency,
                                    from_timestamp: str,
                                    to_timestamp: str) -> dict:
        """Get historical market data include price, market cap, and 24h volume 
           within a range of timestamp (granularity auto)"""
        url: str = f"/coins/{id}/market_chart/range"
        parameters: dict = {"vs_currency": vs_currency, "from": from_timestamp,
                            "to": to_timestamp}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_ohlc(self, id: str, vs_currency, days: str = 'max') -> list:
        """Get coin's OHLC"""
        url: str = f"/coins/{id}/ohlc"
        parameters: dict = {"vs_currency": vs_currency, "days": days}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_info_from_contract_address_by_id(self, id: str,
                                                  contract_address: str) -> dict:
        """Get coin info from contract address"""
        url: str = f"/coins/{id}/contract/{contract_address}"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_coin_market_chart_from_contract_address_by_id(self, id: str,
                                                          contract_address: str,
                                                          vs_currency: str,
                                                          days: str = "max") -> dict:
        """Get historical market data include price, market cap, and 24h volume 
           (granularity auto) from a contract address"""
        url: str = f"/coins/{id}/contract/{contract_address}/market_chart"
        parameters: dict = {"vs_currency": vs_currency, "days": days}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_coin_market_chart_range_from_contract_address_by_id(self, id: str,
                                                                contract_address: str,
                                                                vs_currency: str,
                                                                from_timestamp: str,
                                                                to_timestamp: str) -> dict:
        """Get historical market data include price, market cap, and 24h volume 
        within a range of timestamp (granularity auto) from a contract address"""
        url: str = f"/coins/{id}/contract/{contract_address}/market_chart/range"
        parameters: dict = {"vs_currency": vs_currency, "from": from_timestamp,
                            "to": to_timestamp}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_asset_platforms(self) -> list:
        """List all asset platforms (Blockchain networks)"""
        url: str = "/asset_platforms"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_all_categories_list(self) -> list:
        """List all categories"""
        url: str = "/coins/categories/list"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_all_categories(self, order: str = "market_cap_desc") -> list:
        """List all categories"""
        url: str = "/coins/categories"
        parameters: dict = {"order": order}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_all_exchanges_list(self, *, per_page: int = 100, page: int = 1) -> list:
        """List all exchanges"""
        url: str = "/exchanges"
        parameters: dict = {"per_page": per_page, "page": page}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_all_exchanges_by_id_name_list(self) -> list:
        """List all supported markets id and name (no pagination required)"""
        url: str = "/exchanges/list"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_exchange_by_id(self, id: str = "binance") -> dict:
        """Get exchange volume in BTC and top 100 tickers only"""
        url: str = f"/exchanges/{id}"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_exchange_tickers_by_id(self, id: str = "binance", *, coin_ids: str,
                                   include_exchange_logo: bool = True, page: int = 1,
                                   depth: bool = False,
                                   order: str = "trust_score_desc") -> dict:
        """Get exchange tickers (paginated, 100 tickers per page)"""
        url: str = f"/exchanges/{id}/tickers"
        parameters: dict = {"coin_ids": coin_ids,
                            "include_exchange_logo": include_exchange_logo,
                            "page": page, "depth": depth, "order": order}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_exchange_volume_chart_by_id(self, id: str = "binance", days: int = 1) -> list:
        """Get volume_chart data for a given exchange"""
        url: str = f"/exchanges/{id}/volume_chart"
        parameters: dict = {"id": id, "days": days}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_indexes(self, *, per_page: int = 100, page: int = 1) -> list:
        """List all market indexes"""
        url: str = f"/indexes"
        parameters: dict = {"per_page": per_page, "page": page}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_indexes_by_market_id_and_index_id(self, market_id: str, id: str):
        """get market index by market id and index id"""
        url: str = f"/indexes/{market_id}/{id}"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_indexes_list(self) -> list:
        """list market indexes id and name"""
        url: str = f"/indexes/list"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_derivatives(self, *, include_tickers: str = "all") -> list:
        """List all derivative tickers"""
        url: str = f"/derivatives"
        parameters: dict = {"include_tickers": include_tickers}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_derivatives_exchanges(self, *, order: str = "name_asc",
                                  per_page: int = 100, page: int = 1) -> list:
        """List all derivative exchanges"""
        url: str = f"/derivatives/exchanges"
        parameters: dict = {"order": order, "per_page": per_page, "page": page}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_derivatives_exchanges_by_id(self, id: str, *,
                                        include_tickers: str = "all") -> list:
        """show derivative exchange data"""
        url: str = f"/derivatives/exchanges/{id}"
        parameters: dict = {"include_tickers": include_tickers}
        api_url: str = self.__genr_api_url(url, parameters)
        return self.__request(api_url)

    def get_derivatives_list(self, *, include_tickers: str = "all") -> list:
        """List all derivative exchanges name and identifier"""
        url: str = f"/derivatives/exchanges/list"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def get_exchange_rates(self) -> dict:
        """Get BTC-to-Currency exchange rates"""
        url: str = f"/exchange_rates"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)

    def search(self, query: str) -> dict:
        """Search for coins, categories and markets on CoinGecko"""
        url: str = f"/exchange_rates?{query}"
        api_url: str = self.__genr_api_url(url)
        return self.__request(api_url)
