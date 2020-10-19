"""This module provides functions for downloading and creating options an watchlist."""

from concurrent.futures import as_completed, ThreadPoolExecutor
from typing import List

import typer
from yfs import get_options_page
from yfs.options import OptionsChain

from .options import OptionsData
from .tradingview import TradingViewWatchlist

PROGRESSBAR_LABEL = "Downloading Options Data..."


def normal(tradingview_watchlist: TradingViewWatchlist, days: int) -> List[OptionsChain]:
    """Download option data for each symbol in a TradingView watchlist.

    This is the standard download method. This download method does not use thread or proxies.

    Args:
        tradingview_watchlist (TradingViewWatchlist): A watchlist exported from tradingview.
        days (int): Minimum days left until expiration.
    """
    option_chains = []

    with typer.progressbar(tradingview_watchlist, label=PROGRESSBAR_LABEL) as progress:
        for symbol in progress:
            try:
                chain = get_options_page(
                    symbol.symbol, after_days=days, first_chain=True, page_not_found_ok=True
                )

                if chain:
                    option_chains.append(OptionsData.from_options_page(chain))

            except Exception as exc:  # pylint: disable=broad-except
                typer.echo(exc)

    return option_chains


def threaded(
    tradingview_watchlist: TradingViewWatchlist, days: int, max_workers: int
) -> List[OptionsChain]:
    """Download option data for each symbol in a TradingView watchlist.

    This download method will use threads to speed up the download process.
    This method has a higher chance of hitting rate-limits.

    Args:
        tradingview_watchlist (TradingViewWatchlist): A watchlist exported from tradingview.
        days (int): Minimum days left until expiration.
        max_workers (int): Max thread count for the ThreadPoolExecutor to use.
    """
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

                except Exception as exc:  # pylint: disable=broad-except
                    typer.echo(exc)

    return option_chains


def whaor(
    tradingview_watchlist: TradingViewWatchlist, days: int, max_workers: int, onion_count: int
) -> List[OptionsChain]:
    """Download option data for each symbol in a TradingView watchlist.

    This download method will use threads to speed up the download process.
    Additionally, this method will use requests_whaor to proxy each request to avoid rate-limits.

    Args:
        tradingview_watchlist (TradingViewWatchlist): A watchlist exported from tradingview.
        days (int): Minimum days left until expiration.
        max_workers (int): Max thread count for the ThreadPoolExecutor to use.
    """
    from requests_whaor import RequestsWhaor  # pylint: disable=import-outside-toplevel

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

                    except Exception as exc:  # pylint: disable=broad-except
                        typer.echo(exc)

    return option_chains
