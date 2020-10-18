from options_reticle.watchlist import Watchlist
from options_reticle.paths import PROJECT_ROOT_PATH
from pprint import pprint
from pathlib import Path
import typer

from bullet import Bullet, SlidePrompt, Check, Input, YesNo, Numbers, ScrollBar, VerticalPrompt
from bullet import styles
from bullet import colors


def main(
    watchlist: Path = typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
):
    watchlist = Watchlist.import_from_tradingview_watchlist(location=watchlist)
    watchlist.filter_by_acceptable()

    print(watchlist.describe())
    estimated_scripts = round(len(watchlist) / 200)
    print(f"ESTIMATED NUMBER OF SCRIPTS: {estimated_scripts}")


typer.run(main)

# watchlist_path = PROJECT_ROOT_PATH / "watchlist.txt"
# watchlist_path = PROJECT_ROOT_PATH / "watchlist_mini.txt"
#
# watchlist = Watchlist.import_from_tradingview_watchlist(location=watchlist_path)
# pprint(watchlist.dict())
# # watchlist.filter_by_exchange("NYSE")
# watchlist.filter_by_acceptable()
# pprint(watchlist.dict())
#
# for ticker in watchlist:
#     print(ticker.json())
#
# for chunk in watchlist.iter_chunks():
#     print(len(chunk))
#
