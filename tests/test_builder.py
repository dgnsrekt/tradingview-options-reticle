import pytest
import pendulum

from options_reticle.options import OptionsWatchlist
from options_reticle.paths import TESTS_PATH
from options_reticle.builder import build_script

from pytest_regressions import data_regression  # noqa: F401


@pytest.fixture
def options_data_fixture():
    watchlist_path = TESTS_PATH / "test_data" / "test_option_data.toml"

    assert watchlist_path.exists()

    watchlist = OptionsWatchlist.from_toml(watchlist_path)
    watchlist.sort()

    return watchlist


def test_builder(options_data_fixture, data_regression):
    watchlist = options_data_fixture
    processed_date = pendulum.datetime(2020, 10, 18, tz="UTC")
    version = "0.2.0"

    script = build_script(watchlist, version, processed_date)
    data_regression.check(script)
