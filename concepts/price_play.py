from options_reticle.quote import get_quotes
from options_reticle.watchlist import Watchlist
from options_reticle.paths import PROJECT_ROOT_PATH
from options_reticle.config import MINIMUM_DAYS, WAIT_TIME
from options_reticle.expiration import get_expiration_data
from options_reticle.proxy import proxy_generator

from pprint import pprint
from pathlib import Path
import pendulum
import time
import enlighten


def wait(minutes, description):
    wait_time = minutes * 60
    print(f"waiting {wait_time} minutes")
    print("I'm sorry for this painful wait but the rate limit on yahoo finance very sensitive.")
    print("Without this wait there is a good chance you may get many failed downloads")
    print("If you are getting a lot of download fails or missing data.")
    print("Please increase the wait time by a minute.")

    pbar = enlighten.Counter(total=wait_time, desc=description, unit="seconds")
    for num in range(wait_time):
        time.sleep(1)
        pbar.update()


watchlist_path = PROJECT_ROOT_PATH / "watchlist_mini.txt"
watchlist_path = PROJECT_ROOT_PATH / "watchlist.txt"

watchlist = Watchlist.import_from_tradingview_watchlist(location=watchlist_path)

watchlist.filter_by_acceptable()
symbols = watchlist.get_symbols()

# wait(WAIT_TIME, "waiting before downloading quote data.")
print("Downloading quote data.")
quote_data = get_quotes(symbols)


# wait(WAIT_TIME, "waiting before downloading expiration data.")
PROCESS_DATE = pendulum.now().date()
filter_date = PROCESS_DATE.add(days=MINIMUM_DAYS)

exp_data = get_expiration_data(symbols)
pprint(exp_data)

# tickers = yahoo_client.Tickers(symbols)
# print(tickers.tickers[0].options)
# ticker = yahoo_client.Ticker("GOOGL")
# print(ticker.options)


# time.sleep(30)
# exp_data = filter_all_expirations(symbols, exp_data, filter_date, strict=False)
#
# watchlist.update_quotes(quote_data)
# watchlist.update_expiration_data(exp_data)


# print(watchlist.json(indent=4))
