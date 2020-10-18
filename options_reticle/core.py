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
        option_chains = downloader.threaded(watchlist, days, max_workers)
    elif mode == Mode.whaor:
        option_chains = downloader.whaor(watchlist, days, max_workers, onion_count)
    else:
        option_chains = downloader.normal(watchlist, days)

    downloader.finalize(option_chains, days, output)


build_options = {
    "options_data_input_path": typer.Option(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        writable=False,
        readable=True,
        resolve_path=True,
    )
}


@app.command()
def build(options_data_input_path: Path = build_options["options_data_input_path"]):
    """Builds Options Reticle Scripts from options data."""

    watchlist = OptionsWatchlist.from_toml(options_data_input_path)
    watchlist.sort()
    processed_date = pendulum.now(tz="utc")
    output_path = options_data_input_path.parent
    timestamp = watchlist.meta_data.download_timestamp
    days = watchlist.meta_data.days

    for index, watchlist_chunk in enumerate(watchlist.chunked()):
        filename = output_path / f"options_reticle_script_{timestamp}_{days}_{index}.pine"

        script = build_script(watchlist_chunk, __version__, processed_date)

        with open(filename, mode="w") as file:
            file.write(script)

        typer.echo(f"Version: {__version__}")
        typer.echo(f"Processed Date: {processed_date}")
        typer.echo(f"Symbol Count: {len(watchlist_chunk)}")
        typer.echo(f"Symbols: {watchlist_chunk.symbol_range}")
        typer.echo("META DATA")
        typer.echo("=========")
        typer.echo(watchlist.meta_data.json(indent=4))
        typer.echo(f"Output: {filename}")
        typer.echo()
