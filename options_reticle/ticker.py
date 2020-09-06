from pydantic.dataclasses import dataclass
from pydantic import BaseModel as Base
from typing import Optional, List
from pendulum.datetime import Date, DateTime
from enum import Enum, auto
import pendulum


class OptionProcessPriority(Enum):
    delta = auto()
    dollar = auto()


class OptionData(Base):
    call: Optional[float] = None
    put: Optional[float] = None


class TickerData(Base):
    symbol: str
    exchange: str
    expiration: Optional[Date] = None
    last_price: Optional[float] = None

    dollar: OptionData = OptionData()
    delta: OptionData = OptionData()

    return_data: Optional[str] = None

    @classmethod
    def parse_from_watchlist(cls, ticker: str):  # from_watchlist
        exchange, symbol = ticker.split(":")
        return TickerData(symbol=symbol.strip(), exchange=exchange.strip())

    def update_dollar(self, call, put):
        self.dollar = OptionData(call=call, put=put)

    def update_delta(self, call, put):
        self.delta = OptionData(call=call, put=put)

    def convert_datetime_for_tradingview(self):
        return self.expiration.year, self.expiration.month, self.expiration.day

    def process_call_put_data(self, priority: OptionProcessPriority):
        if priority == OptionProcessPriority.delta:
            call = self.delta.call if self.delta.call else 0.0
            put = self.delta.put if self.delta.put else 0.0

            if not call:
                call = self.dollar.call if self.dollar.call else 0.0
            if not put:
                put = self.dollar.put if self.dollar.put else 0.0

        else:
            call = self.dollar.call if self.dollar.call else 0.0
            put = self.dollar.put if self.dollar.put else 0.0

            if not call:
                call = self.delta.call if self.delta.call else 0.0
            if not put:
                put = self.delta.put if self.delta.put else 0.0

        return call, put

    def create_return_data(self):  # most common as input
        year, month, day = self.convert_datetime_for_tradingview()
        call, put = self.process_call_put_data(priority=OptionProcessPriority.delta)
        # NOTE: decide priorty arg env vs input arg or **kwarg

        data = str([year, month, day, call, put])
        self.return_data = data


class Watchlist(Base):
    watchlist: List[TickerData]

    # get_most_common datetime
    # use counter

    def create_return_data(self):
        for ticker in self.watchlist:
            ticker.create_return_data()  # add a most common datetime

    def __len__(self):
        return len(self.watchlist)

    def join_tickers(self):
        return " ".join([ticker.symbol for ticker in self.watchlist])

    def describe(self):
        head = self.watchlist[0].symbol
        tail = self.watchlist[-1].symbol
        return f"{head} -> {tail}"
