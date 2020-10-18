from .tradingview import TradingViewWatchlist
from .paths import PROJECT_ROOT_PATH
from .options import OptionsData, OptionsWatchlist

from yfs import get_options_page
import typer

from concurrent.futures import as_completed, ThreadPoolExecutor

PROGRESSBAR_LABEL = "Downloading Options Data..."


def normal(watchlist_location, days, output_location):

    tradingview_watchlist = TradingViewWatchlist.from_file(watchlist_location)

    option_chains = []

    with typer.progressbar(tradingview_watchlist, label=PROGRESSBAR_LABEL) as progress:
        for symbol in progress:
            try:
                chain = get_options_page(
                    symbol.symbol, after_days=days, first_chain=True, page_not_found_ok=True
                )

                if chain:
                    option_chains.append(OptionsData.from_options_page(chain))
            except Exception as exc:
                print(exc)

    options_watchlist = OptionsWatchlist(watchlist=option_chains)

    options_watchlist.to_toml(output_location)


def threaded(watchlist_location, days, output_location, max_workers):

    tradingview_watchlist = TradingViewWatchlist.from_file(watchlist_location)

    option_chains = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(
                get_options_page,
                symbol.symbol,
                after_days=days,
                first_chain=True,
                page_not_found_ok=True,
            )
            for symbol in tradingview_watchlist
        ]

        with typer.progressbar(length=len(futures), label=PROGRESSBAR_LABEL) as progress:
            for future in as_completed(futures):
                try:
                    chain = future.result(timeout=60)
                    progress.update(1)

                    if chain:
                        option_chains.append(OptionsData.from_options_page(chain))

                except Exception as exc:
                    print(exc)

    options_watchlist = OptionsWatchlist(watchlist=option_chains)

    options_watchlist.to_toml(output_location)


def whaor(watchlist_location, days, output_location, max_workers, onion_count):
    from requests_whaor import RequestsWhaor

    tradingview_watchlist = TradingViewWatchlist.from_file(watchlist_location)

    option_chains = []

    with RequestsWhaor(
        onion_count=onion_count, start_with_threads=True, max_threads=max_workers
    ) as session:

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(
                    get_options_page,
                    symbol.symbol,
                    after_days=days,
                    first_chain=True,
                    page_not_found_ok=True,
                    session=session,
                )
                for symbol in tradingview_watchlist
            ]

            with typer.progressbar(length=len(futures), label=PROGRESSBAR_LABEL) as progress:
                for future in as_completed(futures):
                    try:
                        chain = future.result(timeout=60)
                        progress.update(1)

                        if chain:
                            option_chains.append(OptionsData.from_options_page(chain))

                    except Exception as exc:
                        print(exc)

    options_watchlist = OptionsWatchlist(watchlist=option_chains)

    options_watchlist.to_toml(output_location)
