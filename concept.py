from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import date
from pprint import pprint
import yfinance as yf
import pendulum


# IDEA: PROCESS_DATE LAST MONDAY
# IDEA: name TradingView_Options_Reticle

#
# @dataclass
# class OptionData:
# option_type: OptionType # enum
#     itm: float
#     atm: float
#     otm: float
#
#
@dataclass
class TickerData:
    symbol: str
    exchange: str
    expiration: date = None
    # option_data: list[]
    # call_option_data: Optional[OptionData] = None
    # put_option_data: Optional[OptionData] = None

    @classmethod
    def parse_watchlist(cls, ticker):
        exchange, symbol = ticker.split(":")
        return TickerData(symbol=symbol, exchange=exchange)


watchlist = Path("watchlist.txt")
assert watchlist.exists()

with open(watchlist) as file:
    watchlist = file.read()

parsed = sorted(
    [TickerData.parse_watchlist(ticker) for ticker in watchlist.split(",")],
    key=lambda ticker_data: ticker_data.symbol,
)

pprint(parsed)


# ALL_EXCHANGES = ["BATS", "OTC", "NYSE", "NASDAQ", "AMEX", "CBOE"]
# ALLOWED_EXCHANGES = ["NYSE", "NASDAQ", "AMEX", "CBOE"]
#
# filtered_by_exchange = filter(lambda x: x.exchange in ALLOWED_EXCHANGES, parsed)
# filtered_by_exchange = list(filtered_by_exchange)
#
# sorted_by_exchange = sorted(filtered_by_exchange, key=lambda x: x.symbol)
#
#
# def get_strike_within_threshold(strike_dates, minimun_days_out=60):
#     now = pendulum.now("UTC").date()
#     threshold = now.add(days=minimun_days_out)
#     s = sorted([pendulum.parse(strike).date() for strike in strike_dates])
#     s = list(filter(lambda d: d >= threshold, s))
#     return s[0]
#
#
# def parse_call_data(options_dataframe, expiration, delta=1):
#     calls = options_dataframe.calls
#     itm_calls = calls["inTheMoney"] == True
#     atm_call = calls[itm_calls].tail(1)
#     atm_idx = atm_call.index
#
#     try:
#         itm = float(calls.loc[atm_idx - delta]["strike"])
#         atm = float(calls.loc[atm_idx]["strike"])
#         otm = float(calls.loc[atm_idx + delta]["strike"])
#         return OptionData(expiration, itm, atm, otm)
#
#     except (KeyError, TypeError):
#         return None
#
#
# def parse_put_data(options_dataframe, expiration, delta=1):
#     puts = options_dataframe.puts
#     itm_puts = puts["inTheMoney"] == True
#     atm_puts = puts[itm_puts].head(1)
#     atm_idx = atm_puts.index
#
#     try:
#         itm = float(puts.loc[atm_idx - delta]["strike"])
#         atm = float(puts.loc[atm_idx]["strike"])
#         otm = float(puts.loc[atm_idx + delta]["strike"])
#         return OptionData(expiration, itm, atm, otm)
#
#     except (KeyError, TypeError):
#         return None
#
#
# debug = 25
#
# for idx, s in enumerate(sorted_by_exchange):
#     if debug:
#         if idx >= debug:
#             break
#
#     expiration = None
#     client = yf.TickerData(s.symbol)
#
#     try:
#         expiration = get_strike_within_threshold(client.options)
#     except IndexError as e:
#         continue
#     print(pendulum.parse(str(expiration)).int_timestamp)
#
#     if expiration:
#         option_chain = client.option_chain(str(expiration))
#         call_data = parse_call_data(option_chain, expiration)
#         put_data = parse_put_data(option_chain, expiration)
#
#         if call_data:
#             s.call_option_data = call_data
#             s.put_option_data = put_data
#             pprint(s)
#
# final = list(
#     filter(
#         lambda x: x.call_option_data is not None or x.put_option_data is not None,
#         sorted_by_exchange,
#     )
# )
# print(final)
