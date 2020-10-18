from options_reticle.watchlist import Watchlist
from options_reticle.paths import PROJECT_ROOT_PATH
from options_reticle.config import MINIMUM_DAYS
from options_reticle.expiration import (
    download_expiration_data,
    filter_expirations,
    download_all_expirations,
)

from pprint import pprint
from pathlib import Path
import pendulum

watchlist_path = PROJECT_ROOT_PATH / "watchlist_mini.txt"
watchlist_path = PROJECT_ROOT_PATH / "watchlist.txt"

watchlist = Watchlist.import_from_tradingview_watchlist(location=watchlist_path)

watchlist.filter_by_acceptable()

watchlist.describe()

estimated_scripts = round(len(watchlist) / 200)

print(f"ESTIMATED NUMBER OF SCRIPTS: {estimated_scripts}")

PROCESS_DATE = pendulum.now().date()
filter_date = PROCESS_DATE.add(days=MINIMUM_DAYS)
print(type(filter_date))

tickers = watchlist.get_symbols()

data = download_all_expirations(tickers)

exp = {}
for ticker in watchlist:
    exp[ticker.symbol] = filter_expirations(data[ticker.symbol], filter_date)

watchlist.update_expiration_data(exp)
print(len(watchlist))
watchlist = Watchlist.from_list([ticker for ticker in watchlist if ticker.expiration is not None])
print(len(watchlist))
# pprint(watchlist.dict())

# for chunk in watchlist.iter_chunks():
# print()
# chunk.describe()
