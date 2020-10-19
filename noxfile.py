import nox

nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ["tests", "cover", "lint"]


@nox.session
def tests(session):
    session.install("poetry")
    session.install("pytest-cov")
    session.run("poetry", "install")
    session.run("poetry", "check")
    session.run("poetry", "run", "pytest", "-vv", "--cov=options_reticle")
    session.notify("cover")


@nox.session
def cover(session):
    session.install("coverage")
    session.run("coverage", "report", "--show-missing", "--fail-under=50")
    session.run("coverage", "erase")


lint_files = [
    "__init__.py",
    "builder.py",
    "core.py",
    "downloader.py",
    "emoji.py",
    "options.py",
    "paths.py",
    "tradingview.py",
]


@nox.session
def lint(session):
    session.install(
        "black",
        "flake8",
        "flake8-import-order",
        "flake8-bugbear",
        "flake8-docstrings",
        "flake8-annotations",
        "pylint",
        "codespell",
    )
    for file_name in lint_files:
        file_path = f"options_reticle/{file_name}"

        session.run("black", "--line-length", "99", "--check", "--quiet", file_path)
        session.run("flake8", "--import-order-style", "google", file_path)
        session.run("pylint", "--disable=E0401,R0903,W0511", file_path)
        session.run("codespell", file_path)
