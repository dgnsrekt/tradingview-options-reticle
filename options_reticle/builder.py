"""This module provides the functions to build the final Tradingview Script."""

from jinja2 import Environment, FileSystemLoader
from pendulum.datetime import DateTime

from .emoji import create_emojis
from .options import OptionsWatchlist
from .paths import TEMPLATES_PATH

file_loader = FileSystemLoader(TEMPLATES_PATH)
environment = Environment(loader=file_loader, keep_trailing_newline=True)

TITLE = "FOMO DRIVEN DEVELOPMENT OPTIONS RETICLE"
SHORT_TITLE = "[FDD] OPTIONS RETICLE"
MAX_BARS_BACK = 90


def build_script(  # pylint: disable=too-many-locals
    watchlist: OptionsWatchlist, version: str, processed_date: DateTime
) -> str:
    """Process the final Tradingview Options Reticle script."""
    head = environment.get_template("head.pine")
    head_section = head.render(
        title=TITLE,
        short_title=SHORT_TITLE,
        ticker_range=watchlist.symbol_range,
        ticker_count=len(watchlist),
        max_bars_back=MAX_BARS_BACK,
        version=version,
        processed_date=processed_date,
        download_timestamp=watchlist.meta_data.download_timestamp,
        days=watchlist.meta_data.days,
    )

    variables = environment.get_template("variables.pine")
    variables_section = variables.render()

    option_function = environment.get_template("option_function.pine")
    option_function_section = option_function.render(watchlist=watchlist)

    reticle = environment.get_template("reticle.pine")
    reticle_section = reticle.render(max_bars_back=MAX_BARS_BACK)

    fill = environment.get_template("fill.pine")
    fill_section = fill.render()

    itm_emojis, otm_emojis = create_emojis()

    emoji = environment.get_template("emoji.pine")
    emoji_section = emoji.render(itm=itm_emojis, otm=otm_emojis)

    label = environment.get_template("label.pine")
    label_section = label.render(
        version=version,
        processed_date=processed_date,
        ticker_range=watchlist.symbol_range,
        download_timestamp=watchlist.meta_data.download_timestamp,
        days=watchlist.meta_data.days,
    )

    return (
        head_section
        + variables_section
        + option_function_section
        + reticle_section
        + fill_section
        + emoji_section
        + label_section
    )
