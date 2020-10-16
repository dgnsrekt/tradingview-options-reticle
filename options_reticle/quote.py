import yfinance as yahoo_client
import numpy as np


# def get_quotes(symbols, proxy=None):
#
#     dataframe = yahoo_client.download(
#         tickers=symbols,
#         period="1d",
#         interval="1d",
#         prepost=False,
#         group_by="ticker",
#         proxy=proxy,
#         threads=True,
#     )
#
#     dataframe = dataframe.replace({np.nan: None})
#
#     quotes = {}
#
#     for symbol in symbols:
#         quote = dataframe[symbol]["Close"].tail(1).values
#
#         if quote:
#             quotes[symbol] = float(quote[0])
#
#     return quotes
