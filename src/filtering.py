import pandas as pd

def filter_data(df: pd.DataFrame):
    return df[df['additional_attributes'].str.contains('is_enabled=Yes')]