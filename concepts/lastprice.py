from pathlib import Path
from pprint import pprint

from options_reticle.watchlist_parser import (
    parse_watchlist,
    filter_watchlist_by_exchange,
    get_last_price_data,
    update_tickers_with_last_price,
)


ACCEPTABLE_EXCHANGES = ["BATS", "OTC", "NYSE", "NASDAQ", "AMEX", "CBOE"]
SELECTED_EXCHANGES = ["NYSE", "NASDAQ", "CBOE"]

watchlist_path = Path("watchlist.txt")
watchlist = parse_watchlist(watchlist_path)

watchlist = filter_watchlist_by_exchange(watchlist, ACCEPTABLE_EXCHANGES)
watchlist = filter_watchlist_by_exchange(watchlist, SELECTED_EXCHANGES)


ticker_data = get_last_price_data(watchlist)
print(type(ticker_data))
watchlist = update_tickers_with_last_price(watchlist, ticker_data)

pprint(watchlist)
print(len(watchlist))
