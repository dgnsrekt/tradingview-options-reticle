from yfs import get_multiple_summary_pages
from yfs import get_options_page

from collections import ChainMap
from typing import List, Optional
from pprint import pprint

from pydantic import BaseModel as Base
from pydantic import Field

import toml

from more_itertools import chunked

from datetime import date

from pathlib import Path


class OptionsData(Base):
    symbol: str
    expiration_date: date
    call_strike: Optional[float]
    put_strike: Optional[float]

    @classmethod
    def from_options_page(cls, page):
        calls = page.calls.dataframe
        puts = page.puts.dataframe

        calls = calls[calls["in_the_money"] == False].head(1).squeeze()
        puts = puts[puts["in_the_money"] == False].tail(1).squeeze()

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
    def call_data(self):
        if self.call_strike:
            return self.call_strike
        return 0.0

    @property
    def put_data(self):
        if self.put_strike:
            return self.put_strike
        return 0.0

    @property
    def year(self):
        return self.expiration_date.year

    @property
    def month(self):
        return self.expiration_date.month

    @property
    def day(self):
        return self.expiration_date.day


class OptionsWatchlist(Base):
    watchlist: List[OptionsData]

    def to_toml(self, location: Path):
        with open(location, mode="w") as file:
            return toml.dump(self.dict(), file)

    @classmethod
    def from_toml(cls, location: Path):
        if not location.exists():
            raise FileNotFoundError(f"{location} not found.")

        with open(location, mode="r") as file:
            watchlist = toml.load(file)

        return cls(**watchlist)

    def __iter__(self):
        return iter(self.watchlist)

    def __len__(self):
        return len(self.watchlist)

    def chunked(self):
        return [OptionsWatchlist(watchlist=chunk) for chunk in chunked(self.watchlist, 200)]

    @property
    def symbol_range(self):
        return f"[{self.watchlist[0].symbol} -> {self.watchlist[-1].symbol}]"
