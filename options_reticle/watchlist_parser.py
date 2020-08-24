from options_reticle.ticker import TickerData
from pathlib import Path
from typing import List


class WatchlistNotFoundError(FileNotFoundError):
    pass


def parse_watchlist(watchlist_location: Path):
    if not watchlist_location.exists():
        raise WatchlistNotFoundError(f"{watchlist_location} not found")

    with open(watchlist_location) as file:
        raw = file.read()

    watchlist = [TickerData.parse_from_watchlist(ticker) for ticker in raw.split(",")]
    return sorted(watchlist, key=lambda ticker: ticker.symbol)


def filter_watchlist_by_exchange(watchlist: List[TickerData], selected_exchanges: List):
    filtered = filter(lambda ticker: ticker.exchange in selected_exchanges, watchlist)
    return sorted(filtered, key=lambda ticker: ticker.symbol)
