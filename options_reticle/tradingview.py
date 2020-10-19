"""This module provides classes and methods for working with exported Tradingview Watchlists."""

from pathlib import Path
from typing import Iterable, List

from pydantic import BaseModel as Base

# ACCEPTABLE_EXCHANGES = ["AMEX", "BATS", "CBOE", "NASDAQ", "NYSE", "OTC"]


class TradingViewTicker(Base):
    """Single ticker from an exported TradingView watchlist.

    Attributes:
        symbol (str): ticker symbol.
        exchange (str): exchange the ticker symbol is on.
    """

    symbol: str
    exchange: str

    @classmethod
    def from_str(cls, ticker: str) -> "TradingViewTicker":
        """Create a TradingViewTicker object from parsing a string."""
        exchange, symbol = ticker.strip().split(":")
        return cls(symbol=symbol, exchange=exchange)


class TradingViewWatchlist(Base):
    """Multiple ticker watchlist exported from a TradingView watchlist.

    Attributes:
        watchlist (List[TradingViewTicker]): List of TradingViewTicker objects.

    """

    watchlist: List[TradingViewTicker]

    @classmethod
    def from_str(cls, contents: str) -> "TradingViewWatchlist":
        """Create a TradingViewWatchlist object from parsing a string of tickers."""
        try:
            contents = [TradingViewTicker.from_str(ticker) for ticker in contents.split(",")]

        except ValueError as error:
            msg = "Make sure the watchlist is properly formatted."
            raise ValueError(msg) from error

        contents = sorted(contents, key=lambda ticker: ticker.symbol)
        return cls(watchlist=contents)

    @classmethod
    def from_file(cls, location: Path) -> "TradingViewWatchlist":
        """Parse a watchlist file exported from TradingView."""
        if not location.exists():
            raise FileNotFoundError(f"{location} not found.")

        with open(location, mode="r") as file:
            contents = file.read()

        return cls.from_str(contents)

    def __len__(self) -> int:
        """Count of tickers in the watchlist."""
        return len(self.watchlist)

    def __iter__(self) -> Iterable[List[TradingViewTicker]]:
        """Iterate over the tickers in the watchlist."""
        return iter(self.watchlist)
