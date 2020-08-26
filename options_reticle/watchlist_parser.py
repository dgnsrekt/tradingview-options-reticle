from options_reticle.ticker import TickerData
from pandas import DataFrame
from pathlib import Path
from typing import List
import yfinance as yahoo_client


class WatchlistNotFoundError(FileNotFoundError):
    pass


def parse_watchlist(watchlist_location: Path):
    if not watchlist_location.exists():
        raise WatchlistNotFoundError(f"{watchlist_location} not found")

    with open(watchlist_location) as file:
        raw = file.read()

    watchlist = [TickerData.parse_from_watchlist(ticker) for ticker in raw.split(",")]
    return sorted(watchlist, key=lambda ticker: ticker.symbol)


def filter_watchlist_by_exchange(watchlist: List[TickerData], selected_exchanges: List):
    filtered = filter(lambda ticker: ticker.exchange in selected_exchanges, watchlist)
    return sorted(filtered, key=lambda ticker: ticker.symbol)


def get_last_price_data(watchlist: List[TickerData]):
    tickers = " ".join([ticker.symbol for ticker in watchlist])

    data = yahoo_client.download(
        tickers=tickers, period="1d", interval="1d", prepost=False, group_by="ticker"
    )
    return data


def update_tickers_with_last_price(watchlist: List[TickerData], ticker_data: DataFrame):
    for ticker in watchlist:
        raw = ticker_data[ticker.symbol]["Close"][0]
        price = float(round(raw, ndigits=2))

        if price > 0:
            ticker.last_price = price

    return watchlist
