from options_reticle.database import SymbolsDatabase
from options_reticle.watchlist import Watchlist
from options_reticle.paths import PROJECT_ROOT_PATH
from options_reticle.quote import get_quotes
import enlighten
import time


def wait(minutes):
    wait_time = minutes * 60
    pbar = enlighten.Counter(total=wait_time, desc="waiting", unit="seconds")
    for num in range(wait_time):
        time.sleep(1)
        pbar.update()


location = PROJECT_ROOT_PATH / "watchlist.txt"

watchlist = Watchlist.import_from_tradingview_watchlist(location=location)
watchlist.filter_by_acceptable()

for ticker in watchlist:
    SymbolsDatabase.add_symbol(ticker.symbol, ticker.exchange)
#
# get_quotes(watchlist.get_symbols())
# get_quotes(watchlist.get_symbols())
# get_quotes(watchlist.get_symbols())
get_quotes(watchlist.get_symbols())
get_quotes(watchlist.get_symbols())

passes = 3  # get from config
for pass_ in range(passes):
    print("pass:", pass_)
    symbols = SymbolsDatabase.get_all_symbols_without_quotes()
    print(f"Found {len(symbols)} symbols without quote data.")

    if pass_ > 0:
        wait(4)

    if symbols:
        quote_data = get_quotes(symbols)
        SymbolsDatabase.update_symbols_with_quotes(quote_data)

    else:
        print("No symbols found without quote data.")
        break


print("done")
