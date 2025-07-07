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
