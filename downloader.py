from pathlib import Path
from pprint import pprint

from options_reticle.ticker import TickerData
from options_reticle.watchlist_parser import (
    parse_watchlist,
    filter_watchlist_by_exchange,
    get_last_price_data,
    update_tickers_with_last_price,
)
from typing import List, Tuple
from enum import IntEnum

import pendulum
from pendulum.datetime import Date
import enlighten


ACCEPTABLE_EXCHANGES = ["BATS", "OTC", "NYSE", "NASDAQ", "AMEX", "CBOE"]
SELECTED_EXCHANGES = ["NYSE", "NASDAQ", "CBOE"]

watchlist_path = Path("watchlist_mini.txt")
watchlist_path = Path("watchlist.txt")
watchlist = parse_watchlist(watchlist_path)

pprint(watchlist)
print(len(watchlist))

watchlist = filter_watchlist_by_exchange(watchlist, ACCEPTABLE_EXCHANGES)
watchlist = filter_watchlist_by_exchange(watchlist, SELECTED_EXCHANGES)


PROCESS_START_DATE = pendulum.now("UTC").date()

SELECTED_MINIMUM_DAYS = 60
ACCEPTABLE_MINIMUM_DAYS = [30, 45, 60, 90, 120]

# assert minimum_days in ACCEPTABLE_MINIMUM_DAYS // should be prior to function call


def filter_option_expiration_dates(expirations: Tuple[str], min_days: int, start_date: Date):
    threshold = start_date.add(days=min_days)
    sorted_dates = sorted([pendulum.parse(_date).date() for _date in expirations])
    filterd_dates = filter(lambda _date: _date >= threshold, sorted_dates)
    return list(filterd_dates)


from pandas import DataFrame


def clean_option_dataframe(option_dataframe: DataFrame):
    columns = ["strike", "inTheMoney"]
    calls = option_dataframe.calls[columns]
    puts = option_dataframe.puts[columns]

    columns = ["strike", "itm"]
    calls.columns = columns
    puts.columns = columns

    return calls, puts


def get_call_strike(call_dataframe, max_depth):
    itm_options = call_dataframe["itm"] == True
    atm = call_dataframe[itm_options].tail(1)

    for d in range(max_depth, 0, -1):
        try:
            strike = float((call_dataframe.loc[atm.index + d]["strike"]))

        except (KeyError, TypeError):
            continue

        if strike:
            return strike

    return None


def get_call_strike_from_price(call_dataframe, price, dollar_threshold=1):
    otm_options = call_dataframe["itm"] == False
    for idx, otm in call_dataframe[otm_options].iterrows():
        strike = float(otm["strike"])
        if (strike - price) >= dollar_threshold:
            return strike


def get_put_strike_from_price(put_dataframe, price, dollar_threshold=1):
    otm_options = put_dataframe["itm"] == False
    for idx, otm in put_dataframe[otm_options].iloc[::-1].iterrows():
        strike = float(otm["strike"])
        if (price - strike) >= dollar_threshold:
            return strike


def get_put_strike(put_dataframe, max_depth):
    itm_options = put_dataframe["itm"] == False
    atm = put_dataframe[itm_options].tail(1)

    for d in range(max_depth, 0, -1):
        try:
            strike = float((put_dataframe.loc[atm.index - d]["strike"]))

        except (KeyError, TypeError):
            continue

        if strike:
            return strike

    return None


import yfinance as yahoo_client


def get_options_data(ticker: TickerData, max_std_otm=1):
    client = yahoo_client.Ticker(ticker.symbol)

    try:
        option_dates = client.options
    except IndexError:
        return None

    if len(option_dates) < 1:
        return None

    option_dates = filter_option_expiration_dates(
        option_dates, SELECTED_MINIMUM_DAYS, PROCESS_START_DATE
    )
    expiration_date = option_dates[0]

    option_dataframe = client.option_chain(str(expiration_date))
    call_data, put_data = clean_option_dataframe(option_dataframe)

    if ticker.last_price is not None:
        call_price = get_call_strike_from_price(call_data, ticker.last_price)
        put_price = get_put_strike_from_price(put_data, ticker.last_price)
    else:
        print(ticker.symbol, "using std")
        call_price = get_call_strike(call_data, max_depth=max_std_otm)
        put_price = get_put_strike(put_data, max_depth=max_std_otm)

    return expiration_date, call_price, put_price


ticker_data = get_last_price_data(watchlist)
watchlist = update_tickers_with_last_price(watchlist, ticker_data)

pprint(watchlist)
#
# pbar = enlighten.Counter(total=len(watchlist), unit="symbols")
# for ticker in watchlist:
#     pbar.desc = ticker.symbol
#     option_data = get_options_data(ticker)
#     if option_data:
#         ticker.update_options_data(*option_data)
#     pbar.update()
#
# pprint(watchlist)
