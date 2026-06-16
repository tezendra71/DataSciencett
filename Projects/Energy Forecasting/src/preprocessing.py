import pandas as pd


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean dataset: handle missing values and duplicates."""

    df = df.drop_duplicates()

    # Fill missing values
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].fillna(df[col].mode()[0])
        else:
            df[col] = df[col].fillna(df[col].median())

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date and create time features."""

    df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()

    if "day_in_week" in df.columns:
        df = df.drop(columns=["day_in_week"])

    df = pd.get_dummies(df, columns=["weekday"], drop_first=False, dtype=int)

    return df