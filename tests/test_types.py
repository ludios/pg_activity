import pytest

from pgactivity.config import Flag
from pgactivity.types import UI, Filters, QueryMode


def test_filters_from_options():
    f = Filters.from_options(["dbname:postgres"])
    assert f == Filters(dbname="postgres")


@pytest.mark.parametrize(
    "key, value",
    [
        # Linux PID_MAX_LIMIT on 64-bit systems
        ("pid", 4194304),
        # Largest 32-bit transaction ID
        ("xmin", 2**32 - 1),
    ],
)
def test_column_fits_largest_value(key, value):
    """Columns must be wide enough for their largest possible value, otherwise
    subsequent columns get shifted and table alignment breaks.
    """
    ui = UI.make(flag=Flag.all(), query_mode=QueryMode.activities)
    column = ui.column(key)
    assert len(column.render(value)) == len(column.title_render()) == column.min_width
