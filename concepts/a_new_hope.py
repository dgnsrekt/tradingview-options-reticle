from yfs import get_multiple_summary_pages
from yfs import get_options_page

from collections import ChainMap
from pprint import pprint

from pydantic import BaseModel as Base
from pydantic import Field

from datetime import date


class Ticker(Base):
    symbol: str
    expiration_date: date
    call: float = Field(alias="call_strike")
    put: float = Field(alias="put_strike")

    @classmethod
    def from_options_page(cls, page):
        calls = page.calls.dataframe
        puts = page.puts.dataframe

        calls = calls[calls["in_the_money"] == False].head(1).squeeze().to_dict()
        puts = puts[puts["in_the_money"] == False].tail(1).squeeze().to_dict()

        calls["call_strike"] = calls["strike"]
        puts["put_strike"] = puts["strike"]

        options = dict(ChainMap(calls, puts))

        return cls(**options)


for symbols in ["AAPL", "SPY"]:
    oc = get_options_page(symbols, after_days=90, first_chain=True)
    print(Ticker.from_options_page(oc).json(indent=4))
