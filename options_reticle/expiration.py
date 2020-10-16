""" Used for downloading, filtering, and processing expiration data """

import yfinance as yahoo_client
import pendulum
from pendulum.date import Date
from typing import Tuple, List
from loguru import logger
from multiprocessing import Pool, cpu_count
from collections import ChainMap
import time
from random import shuffle


def get_expiration_data(symbols):
    shuffle(symbols)
    clients = yahoo_client.Tickers(" ".join(symbols))
    data = {}
    for ticker in clients.tickers:
        logger.debug(f"Getting expiration data for {ticker.ticker}.")
        try:
            expirations = ticker.options
            print(ticker.ticker, expirations)
            data[ticker.ticker] = expirations if expirations else None
        except IndexError as e:
            pass
    return data


def download_all_expirations(tickers: List[str]):
    # cores = min([cpu_count(), 4])
    # logger.debug(f"Using {cores} cores to download expiration data.")
    # time.sleep(1)

    # data = Pool(cores).map(get_expirations, tickers)
    # data = list(filter(lambda d: d is not None, data))

    data = []

    for ticker in tickers:
        data.append(get_expirations(ticker))

    return data


def filter_expirations(expirations: Tuple[str], filter_date: Date, strict=True):
    if not expirations:
        return None

    sorted_dates = sorted([pendulum.parse(_date).date() for _date in expirations])

    try:
        filterd_dates = list(filter(lambda _date: _date >= filter_date, sorted_dates))
        return filterd_dates[0]

    except IndexError:

        if strict:
            return None
        else:
            return sorted_dates[0]


def filter_all_expirations(symbols, expirations, filter_date, strict=True):
    data = {}
    for symbol in symbols:
        e = expirations.get(symbol)
        data[symbol] = filter_expirations(e, filter_date, strict=strict)
    return data
