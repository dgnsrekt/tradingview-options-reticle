import pytest
import pickle

from options_reticle.options import OptionsWatchlist, OptionsData
from options_reticle.paths import TESTS_PATH

from pytest_regressions import data_regression  # noqa: F401


@pytest.fixture
def options_data_fixture():
    watchlist_path = TESTS_PATH / "test_data" / "test_option_data.toml"
    assert watchlist_path.exists()

    watchlist = OptionsWatchlist.from_toml(watchlist_path)
    watchlist.sort()

    return watchlist


@pytest.fixture
def options_page_pickle_fixture():
    options_chain_data_path = TESTS_PATH / "test_data" / "appl_options_chain_data.pickle"
    assert options_chain_data_path.exists()

    with open(options_chain_data_path, mode="rb") as file:
        options_chain_data = pickle.load(file)

    return options_chain_data


def test_option_data_created_from_option_object(options_page_pickle_fixture):
    option_data = OptionsData.from_options_page(options_page_pickle_fixture)
    assert option_data.call_strike == 120.0
    assert option_data.put_strike == 117.5
    assert option_data.year == 2021
    assert option_data.month == 1
    assert option_data.day == 15


def test_options_watchlist_created_from_file(options_data_fixture, data_regression):
    data_regression.check(options_data_fixture.json())


def test_options_watchlist_symbol_range(options_data_fixture, data_regression):
    result = f"[{options_data_fixture.head} -> {options_data_fixture.tail}]"
    data_regression.check(result)


def test_options_watchlist_len(options_data_fixture, data_regression):
    assert len(options_data_fixture) == 13


def test_options_watchlist_meta_data(options_data_fixture, data_regression):
    data_regression.check(options_data_fixture.meta_data.json())
