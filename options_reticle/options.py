"""This module provides objects for creating and storing Options Watchlists."""

from collections import ChainMap
from pathlib import Path
from typing import Iterable, List, Optional

from more_itertools import chunked
from pendulum.date import Date
from pydantic import BaseModel as Base
from pydantic import validator
import toml
from yfs.options import OptionsChain


class OptionsData(Base):
    """Holds options data.

    Attributes:
        symbol (str): Ticker symbol.
        expiration_date (Date): Date the contract will expire.
        call_strike (Optiona[float]): A call option strike price.
        put_strike (Optiona[float]): A put option strike price.
    """

    symbol: str
    expiration_date: Date
    call_strike: Optional[float] = 0.0
    put_strike: Optional[float] = 0.0

    @validator("symbol")
    def clean_symbol(value: str) -> str:  # pylint: disable=no-self-argument
        """Clean ^ sign from symbol."""
        return value.replace("^", "")

    @classmethod
    def from_options_page(cls, page: OptionsChain) -> Optional["OptionsData"]:
        """Create a OptionsData object from a yfs.OptionsChain object.

        Args:
            page (OptionsChain): Chain of option contracts with the same expiration date.
        """
        calls = page.calls.dataframe
        puts = page.puts.dataframe

        calls = (
            calls[calls["in_the_money"] == False]  # noqa pylint: disable=singleton-comparison
            .head(1)
            .squeeze()
        )
        puts = (
            puts[puts["in_the_money"] == False]  # noqa pylint: disable=singleton-comparison
            .tail(1)
            .squeeze()
        )

        if calls.empty:
            calls = dict()
        else:
            calls = calls.to_dict()
            calls["call_strike"] = calls["strike"]

        if puts.empty:
            puts = dict()
        else:
            puts = puts.to_dict()
            puts["put_strike"] = puts["strike"]

        options = dict(ChainMap(calls, puts))

        if options:
            return cls(**options)

        return None

    @property
    def year(self) -> int:
        """Return the year of expiration."""
        return self.expiration_date.year

    @property
    def month(self) -> int:
        """Return the month of expiration."""
        return self.expiration_date.month

    @property
    def day(self) -> int:
        """Return the day of expiration."""
        return self.expiration_date.day

    def __lt__(self, other: "OptionsData") -> bool:
        """Compare symbol name for sorting."""
        if other.__class__ is self.__class__:
            return self.symbol < other.symbol
        return None


class MetaData(Base):
    """Stores meta data.

    Attributes:
        download_timestamp (int): Time the options data was downloaded.
        days (int): Days til expiration used to filter the options data.
    """

    download_timestamp: int
    days: int


class OptionsWatchlist(Base):
    """Holds a multiple OptionData objects.

    Attributes:
        watchlist (List[OptionsData]): list of OptionsData objects.
        meta_data (MetaData): MetaData object.
    """

    watchlist: List[OptionsData]
    meta_data: MetaData

    def to_toml(self, location: Path) -> None:
        """Dump OptionsWatchlist object to a toml file."""
        with open(location, mode="w") as file:
            return toml.dump(self.dict(), file)

    @classmethod
    def from_toml(cls, location: Path) -> "OptionsWatchlist":
        """Load OptionsWatchlist object from a toml file."""
        if not location.exists():
            raise FileNotFoundError(f"{location} not found.")

        with open(location, mode="r") as file:
            watchlist = toml.load(file)

        return cls(**watchlist)

    def __iter__(self) -> Iterable[List[OptionsData]]:
        """Iterate over the OptionsData objects in the watchlist."""
        return iter(self.watchlist)

    def __len__(self) -> int:
        """Count of OptionsData objects in the watchlist."""
        return len(self.watchlist)

    def chunked(self) -> List["OptionsWatchlist"]:
        """Create a list of OptionsWatchlist chunks with a maximum of 200 tickers."""
        return [
            OptionsWatchlist(watchlist=chunk, meta_data=self.meta_data)
            for chunk in chunked(self.watchlist, 200)
        ]

    def sort(self) -> None:
        """Sort the watchlist by symbol."""
        self.watchlist = sorted(self.watchlist)

    @property
    def head(self) -> str:
        """First ticker in watchlist."""
        return self.watchlist[0].symbol

    @property
    def tail(self) -> str:
        """Last ticker in watchlist."""
        return self.watchlist[-1].symbol
