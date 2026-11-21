<!-- clank-right
languages   = ["python"]
conventions = "upstream"
-->

# This fork

This repository is the user's fork of pg_activity, a `top`-like terminal UI that shows what a PostgreSQL server is doing: `origin` is dalibo/pg_activity, `gh` is the user's fork, ludios/pg_activity, and the branch `prime` carries the fork's commits on top of upstream `master`.

Only this `AGENTS.md` is the fork's own, so change it only in commits that change nothing else. Every other change should stay upstreamable:

- Follow the surrounding upstream code's style: black, isort, flake8, and pyupgrade's `--py39-plus`. The code must still run on Python 3.9 (`requires-python` in `pyproject.toml`).
- A user-visible change may add an entry under an **Unreleased** section at the top of `CHANGELOG.md`; at release time, the maintainers add the entries that are missing, from the git history (see `RELEASE.md`). The version in `pgactivity/__init__.py` changes only in a release.
- A change to a command-line option also changes `README.md` (which shows the `--help` output), `docs/man/pg_activity.pod`, the `docs/man/pg_activity.1` that `docs/man/build-man.sh` makes from it, `tests/test_cli_help.txt` and `tests/test_cli_help_py312.txt`.

# Tests

`pytest` also runs the doctests in `pgactivity/` and in `tests/test_*.txt` (`--doctest-modules` in `pytest.ini`), and it fails on any warning.

The doctests compare whole rendered screens, so a change to a column's width, or to anything else in the layout, changes many expected outputs: in `tests/test_views.txt`, `tests/test_ui.txt`, `tests/test_scroll.txt`, `tests/test_views.py`, and the docstrings in `pgactivity/views.py`. Update them to the actual output, keeping the `...` and `<BLANKLINE>` markers; `pytest --doctest-continue-on-failure` shows every mismatch in a file instead of only the first.

- Lines of expected output in `tests/test_*.txt` can end in spaces that the test compares (pre-commit's whitespace fixers skip these files): never strip them.
- A query cut off at the terminal's width can end in a fragment that codespell takes for a typo (`USIN`, `nam`, `WHER`): add such a fragment to `--ignore-words-list` in both `tox.ini` and `.pre-commit-config.yaml`.

`tests/test_ui.txt` and `tests/test_data.py` start a temporary PostgreSQL server through pytest-postgresql, which finds `pg_ctl` on the `PATH`. On this machine, two tests in `tests/test_data.py` skip because the fr_FR and zh_TW.EUC-TW locales are missing, and `tests/test_cli_help_py312.txt` skips on Python 3.13 and later.

# Before committing

Run upstream's CI checks, and the tests with both database drivers (psycopg 3 and psycopg2):

	uvx tox -e check-manifest,lint,mypy,py-psycopg3,py-psycopg2

Not `uvx --with tox-uv tox`, which fails here because it looks for a `uv` binary inside uvx's environment. After the first run, `.tox/py-psycopg3/bin/pytest` reruns some of the tests quickly, e.g. `.tox/py-psycopg3/bin/pytest tests/test_views.txt`.
