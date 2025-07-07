import bt
import pandas as pd

from django.db.models import QuerySet


def convert_queryset_to_dataframe(queryset: QuerySet) -> pd.DataFrame:
    """
    Convert a Django QuerySet to a Pandas DataFrame.
    """
    if not queryset:
        return pd.DataFrame()

    # Convert the QuerySet to a DataFrame
    df = pd.DataFrame(list(queryset.values()))

    return df


def serialize_backtest_stats(stats: bt.ffn.core.PerformanceStats) -> dict:
    """
    Serialize bt.ffn.core.PerformanceStats to a dictionary.
    """
    if not stats:
        return {}

    price = stats.prices.copy()
    price.index = price.index.strftime("%Y-%m-%d")
    price_data = price.reset_index().rename(columns={"index": "date"})
    price_data = price_data.rename(columns={stats.name: "price"})

    return {
        "name": stats.name,
        "stats": stats.stats.to_dict(),
        "lookback_returns": stats.lookback_returns.to_dict(),
        "price": price_data.to_dict(orient="records"),
    }
