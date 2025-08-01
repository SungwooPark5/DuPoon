import pytest
import pandas as pd


@pytest.fixture(autouse=True)
def enable_celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.CELERY_TASK_EAGER_PROPAGATES = False


@pytest.fixture
def fake_price_data_df():
    fake_data = pd.DataFrame(
        [[37, 81, 81, 81, 81, 6100], [38, 82, 83, 83, 84, 10000]],
        index=pd.date_range("2022-01-01", periods=2),
        columns=pd.MultiIndex.from_tuples(
            [
                ("Adj Close", "TST"),
                ("Close", "TST"),
                ("High", "TST"),
                ("Low", "TST"),
                ("Open", "TST"),
                ("Volume", "TST"),
            ]
        ),
        dtype=float,
    )
    fake_data.index.name = "Date"
    fake_data.columns.names = ["Price", "Ticker"]

    return fake_data
