from pydantic import BaseModel as Base
from options_reticle.ticker import TickerData
from typing import List
from pathlib import Path
from more_itertools import chunked
from loguru import logger

# from pandas import DataFrame
# from pathlib import Path
# import yfinance as yahoo_client
#
#
class WatchlistNotFoundError(FileNotFoundError):
    pass


class WatchlistFormatError(ValueError):
    pass


#
#

# def filter_watchlist_by_exchange(watchlist: List[TickerData], selected_exchanges: List):
#     filtered = filter(lambda ticker: ticker.exchange in selected_exchanges, watchlist)
#     return sorted(filtered, key=lambda ticker: ticker.symbol)
#
#
# def get_last_price_data(watchlist: List[TickerData]):
#     tickers = " ".join([ticker.symbol for ticker in watchlist])
#
#     data = yahoo_client.download(
#         tickers=tickers, period="1d", interval="1d", prepost=False, group_by="ticker"
#     )
#     return data
#
#
# def update_tickers_with_last_price(watchlist: List[TickerData], ticker_data: DataFrame):
#     for ticker in watchlist:
#         raw = ticker_data[ticker.symbol]["Close"].get(0)
#         price = float(round(raw, ndigits=2))
#
#         if price > 0:
#             ticker.last_price = price
#
#     return watchlist

ACCEPTABLE_EXCHANGES = ["AMEX", "BATS", "CBOE", "NASDAQ", "NYSE", "OTC"]


class Watchlist(Base):
    watchlist: List[TickerData]

    def get_symbols(self):
        return [ticker.symbol for ticker in self.watchlist]

    def update_expiration_data(self, data: dict):
        for ticker in self.watchlist:
            ticker.expiration = data.get(ticker.symbol)

    def update_quotes(self, data: dict):
        for ticker in self.watchlist:
            ticker.last_price = data.get(ticker.symbol)

    @classmethod
    def from_list(cls, watchlist: List[TickerData]):
        return cls(watchlist=watchlist)

    @classmethod
    def from_str(cls, contents: str):
        try:
            contents = [
                TickerData.parse_from_tv_ticker_id(ticker) for ticker in contents.split(",")
            ]
        except ValueError:
            error_msg = "Make sure the watchlist has been exported from tradingview."
            raise WatchlistFormatError(error_msg)

        sorted_contents = sorted(contents, key=lambda ticker: ticker.symbol)
        return cls(watchlist=sorted_contents)

    @classmethod
    def import_from_tradingview_watchlist(cls, location: Path):
        if not location.exists():
            raise WatchlistNotFoundError(f"{location} not found")

        with open(location, mode="r") as file:
            contents = file.read()

        return cls.from_str(contents)

    def filter_by_exchange(self, selected_exchanges: List[str]):
        omitted = filter(lambda ticker: ticker.exchange not in selected_exchanges, self.watchlist)
        omitted = sorted(set([ticker.exchange for ticker in omitted]))

        if omitted:
            logger.info(f"Removing tickers from the following exchange: {omitted}")

        filtered = filter(lambda ticker: ticker.exchange in selected_exchanges, self.watchlist)
        sorted_contents = sorted(filtered, key=lambda ticker: ticker.symbol)

        self.watchlist = list(sorted_contents)

    def filter_by_acceptable(self):
        self.filter_by_exchange(ACCEPTABLE_EXCHANGES)

    def iter_chunks(self, size: int = 200):
        return [Watchlist(watchlist=chunk) for chunk in chunked(self.watchlist, size)]

    @property
    def exchanges(self):
        return sorted(set([ticker.exchange for ticker in self.watchlist]))

    def describe(self):
        return print(f"TICKER COUNT: {len(self)}\nEXCHANGES: {self.exchanges}")

    def __len__(self):
        return len(self.watchlist)

    def __iter__(self):
        return iter(self.watchlist)


# def create_return_data(self):
#     for ticker in self.watchlist:
#         ticker.create_return_data()  # add a most common datetime
#
# def __len__(self):
#     return len(self.watchlist)
#
# def join_tickers(self):
#     return " ".join([ticker.symbol for ticker in self.watchlist])
#
# def describe(self):
#     head = self.watchlist[0].symbol
#     tail = self.watchlist[-1].symbol
#     return f"{head} -> {tail}"
