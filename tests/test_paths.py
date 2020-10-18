import tomlkit

import options_reticle
from options_reticle.paths import PROJECT_ROOT_PATH, SOURCE_ROOT_PATH


def test_sanity():
    pyproject_path = PROJECT_ROOT_PATH / "pyproject.toml"
    assert pyproject_path.exists()

    with open(pyproject_path, mode="r") as file:
        content = tomlkit.parse(file.read())

    assert content["tool"]["poetry"].get("version") is not None


def test_sanity_two():
    assert SOURCE_ROOT_PATH.exists()
