from concurrent.futures import as_completed, ThreadPoolExecutor

from .options import MetaData, OptionsData, OptionsWatchlist
from .paths import PROJECT_ROOT_PATH
from .tradingview import TradingViewWatchlist

import typer
import pendulum
from yfs import get_options_page


PROGRESSBAR_LABEL = "Downloading Options Data..."


def finalize(option_chains, days, output_location):

    download_timestamp = pendulum.now(tz="UTC").int_timestamp

    meta_data = MetaData(download_timestamp=download_timestamp, days=days)

    options_watchlist = OptionsWatchlist(watchlist=option_chains, meta_data=meta_data)

    options_watchlist.to_toml(output_location)


def normal(watchlist_location, days):

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

    return option_chains


def threaded(watchlist_location, days, max_workers):

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

    return option_chains


def whaor(watchlist_location, days, max_workers, onion_count):
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

    return option_chains
