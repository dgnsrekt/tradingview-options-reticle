from pathlib import Path
from pprint import pprint

from options_reticle.ticker import TickerData
from options_reticle.watchlist_parser import parse_watchlist, filter_watchlist_by_exchange
from typing import List, Tuple
from enum import IntEnum

import pendulum
from pendulum.datetime import Date
import enlighten

import yfinance as yahoo_client

ACCEPTABLE_EXCHANGES = ["BATS", "OTC", "NYSE", "NASDAQ", "AMEX", "CBOE"]
SELECTED_EXCHANGES = ["NYSE", "NASDAQ", "CBOE"]

watchlist_path = Path("watchlist.txt")
watchlist = parse_watchlist(watchlist_path)

watchlist = filter_watchlist_by_exchange(watchlist, ACCEPTABLE_EXCHANGES)
watchlist = filter_watchlist_by_exchange(watchlist, SELECTED_EXCHANGES)


def get_last_price_data(watchlist: List[TickerData]):
    tickers = " ".join([ticker.symbol for ticker in watchlist])

    data = yahoo_client.download(
        tickers=tickers, period="1d", interval="1d", prepost=False, group_by="ticker"
    )
    return data


data = get_last_price_data(watchlist)

for ticker in watchlist:
    raw = data[ticker.symbol]["Close"][0]
    price = float(round(raw, ndigits=2))

    if price > 0:
        ticker.last_price = price
    else:
        ticker.last_price = None


pprint(watchlist)
print(len(watchlist))
