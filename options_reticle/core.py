import typer
from pathlib import Path
from enum import Enum
from . import downloader, __version__
from .options import OptionsWatchlist
from .builder import build_script
import pendulum


app = typer.Typer()


class Mode(str, Enum):
    normal = "normal"
    threaded = "threaded"
    whaor = "whaor"


info = {
    "watchlist": "Path to a watchlist.txt file exported from tradingview.",
    "days": "Minimum days before the contract's expiration.",
    "output": "Path to store the options data.",
    "mode": "Method used to download options data.",
    "max_workers": "How many threads to use when downloading with THREADED or WHAOR mode.",
    "onion_count": "How many TOR circuits to use when downloading with WHAOR mode.",
}

download_options = {
    "watchlist": typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
        help=info["watchlist"],
    ),
    "days": typer.Option(60, prompt=info["days"], help=info["days"]),
    "output": typer.Option("option_data.toml", exists=False, help=info["output"]),
    "mode": typer.Option(Mode.normal, prompt=info["mode"], help=info["mode"]),
    "max_workers": typer.Option(4, help=info["max_workers"]),
    "onion_count": typer.Option(4, help=info["onion_count"]),
}


@app.command()
def download(
    watchlist: Path = download_options["watchlist"],
    days: int = download_options["days"],
    output: Path = download_options["output"],
    mode: Mode = download_options["mode"],
    max_workers: int = download_options["max_workers"],
    onion_count: int = download_options["onion_count"],
):
    """Downloads options data based on a tradingview watchlist."""

    if mode == Mode.threaded:
        downloader.threaded(watchlist, days, output, max_workers)
    elif mode == Mode.whaor:
        downloader.whaor(watchlist, days, output, max_workers, onion_count)
    else:
        downloader.normal(watchlist, days, output)


@app.command()
def build(
    input_path: Path = typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    ),
):
    """Builds Options Reticle Scripts from options data."""

    watchlist = OptionsWatchlist.from_toml(input_path)
    processed_date = pendulum.now(tz="utc")
    output_path = input_path.parent

    for index, watchlist_chunk in enumerate(watchlist.chunked()):
        script = build_script(watchlist_chunk, __version__, processed_date)
        filename = output_path / f"options_reticle_script_{index}.pine"

        with open(filename, mode="w") as file:
            file.write(script)
