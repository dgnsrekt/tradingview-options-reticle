import pytest

from options_reticle.tradingview import TradingViewWatchlist
from options_reticle.paths import PROJECT_ROOT_PATH


WATCHLIST_STRING = (
    "NASDAQ:AAPL,NYSE:WORK,NASDAQ:BWAY,NYSE:YRD,"
    "NYSE:WGO,NASDAQ:SOHO,NASDAQ:PDCO,"
    "NASDAQ:AVAV,NYSE:LZB,NASDAQ:FMCI,"
    "NYSE:WTI,NASDAQ:INO,AMEX:GLD,"
    "AMEX:GDX,NYSE:QD\n"
)

BAD_WATCHLIST_STRING = (
    "NASDAQAAPL,NYSEWORK,NASDAQ:BWAY,NYSE:YRD,"
    "NYSE:WGO,NASDAQ:SOHO,NASDAQ:PDCO,"
    "NASDAQAVAV,NYSELZB,FMCI,"
    "NYSE:WTINASDAQ:INOAMEX:GLD,"
    "AMEX:GDXNYSE:QD\n"
)


@pytest.fixture
def watchlist_file_fixture():
    watchlist_path = PROJECT_ROOT_PATH / "tests" / "test_data" / "test_watchlist.txt"

    assert watchlist_path.exists()

    return watchlist_path


@pytest.fixture
def bad_watchlist_file_fixture():
    watchlist_path = PROJECT_ROOT_PATH / "tests" / "test_data" / "bad_test_watchlist.txt"

    assert not watchlist_path.exists()

    return watchlist_path


def test_watchlist_created_from_str():
    watchlist = TradingViewWatchlist.from_str(WATCHLIST_STRING)
    assert len(watchlist) == 15


def test_watchlist_created_from_bad_str_raises_error():
    with pytest.raises(ValueError) as excinfo:
        watchlist = TradingViewWatchlist.from_str(BAD_WATCHLIST_STRING)

    assert "Make sure the watchlist is properly formatted." == str(excinfo.value)


def test_watchlist_created_from_file(watchlist_file_fixture):
    watchlist = TradingViewWatchlist.from_file(watchlist_file_fixture)
    assert len(watchlist) == 15


def test_watchlist_created_from_bad_filepath(bad_watchlist_file_fixture):
    with pytest.raises(FileNotFoundError) as excinfo:
        watchlist = TradingViewWatchlist.from_file(bad_watchlist_file_fixture)

    error_msg = (
        "/home/dgnsrekt/Development/tradingview/tradingview-options-reticle/"
        "tests/test_data/bad_test_watchlist.txt not found."
    )
    assert str(excinfo.value) == error_msg


def test_compare_watchlist(watchlist_file_fixture):
    watchlist_one = TradingViewWatchlist.from_str(WATCHLIST_STRING)
    watchlist_two = TradingViewWatchlist.from_file(watchlist_file_fixture)
    assert watchlist_one == watchlist_two
