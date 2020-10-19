"""This module provides classes and methods for working with exported Tradingview Watchlists."""

from pydantic import BaseModel as Base
from typing import Optional, List
from pathlib import Path
from yfs.options import OptionsChain

ACCEPTABLE_EXCHANGES = ["AMEX", "BATS", "CBOE", "NASDAQ", "NYSE", "OTC"]


class TradingViewTicker(Base):
    symbol: str
    exchange: str

    @classmethod
    def from_str(cls, ticker: str):
        exchange, symbol = ticker.strip().split(":")
        return cls(symbol=symbol, exchange=exchange)


class TradingViewWatchlist(Base):
    watchlist: List[TradingViewTicker]

    @classmethod
    def from_str(cls, contents: str):
        try:
            contents = [TradingViewTicker.from_str(ticker) for ticker in contents.split(",")]

        except ValueError:
            msg = "Make sure the watchlist is properly formatted."
            raise ValueError(msg)

        contents = sorted(contents, key=lambda ticker: ticker.symbol)
        return cls(watchlist=contents)

    @classmethod
    def from_file(cls, location: Path):
        if not location.exists():
            raise FileNotFoundError(f"{location} not found.")

        with open(location, mode="r") as file:
            contents = file.read()

        return cls.from_str(contents)

    def __len__(self):
        return len(self.watchlist)

    def __iter__(self):
        return iter(self.watchlist)
