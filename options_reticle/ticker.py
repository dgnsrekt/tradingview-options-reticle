from pydantic.dataclasses import dataclass
from typing import Optional
from pendulum.datetime import Date


@dataclass
class TickerData:
    symbol: str
    exchange: str
    expiration: Optional[Date] = None
    last_price: Optional[float] = None
    call: Optional[float] = None
    put: Optional[float] = None

    @classmethod
    def parse_from_watchlist(cls, ticker: str):
        exchange, symbol = ticker.split(":")
        return TickerData(symbol=symbol.strip(), exchange=exchange.strip())

    def update_options_data(self, expiration: Date, call: float, put: float):
        self.expiration = expiration
        self.call = call
        self.put = put
