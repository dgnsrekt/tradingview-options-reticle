import pytest

from options_reticle.watchlist import Watchlist
from options_reticle.paths import PROJECT_ROOT_PATH

WATCHLIST_STRING = (
    "NASDAQ:AAPL,NYSE:WORK,NASDAQ:BWAY,NYSE:YRD,"
    "NYSE:WGO,NASDAQ:SOHO,NASDAQ:PDCO,"
    "NASDAQ:AVAV,NYSE:LZB,NASDAQ:FMCI,"
    "NYSE:WTI,NASDAQ:INO,AMEX:GLD,"
    "AMEX:GDX,NYSE:QD\n"
)


@pytest.fixture
def watchlist_file_fixture():
    watchlist_path = PROJECT_ROOT_PATH / "tests" / "test_watchlist.txt"
    assert watchlist_path.exists()
    with open(watchlist_path, mode="r") as file:
        contents = file.read()

    assert contents == WATCHLIST_STRING
    return watchlist_path


def test_watchlist_creation(watchlist_file_fixture):
    watchlist_one = Watchlist.from_str(WATCHLIST_STRING)
    watchlist_two = Watchlist.import_from_tradingview_watchlist(watchlist_file_fixture)
    assert watchlist_one == watchlist_two

    assert len(watchlist_one) == 15
    assert len(watchlist_two) == 15


def test_filter_watchlist_by_exchange():
    before, after = 15, 6
    watchlist = Watchlist.from_str(WATCHLIST_STRING)
    assert len(watchlist) == before
    watchlist.filter_by_exchange("NYSE")
    assert len(watchlist) == after
