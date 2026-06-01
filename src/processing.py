import pandas as pd
def process_data(df: pd.DataFrame):
    required_cols = ['sku', 'name', 'short_description', 'description', 'categories', 'additional_attributes']
    df = df[required_cols]
    df.to_excel('data1.xlsx', index=False)  # Save the data inside of excel file with disabled numerical index (serial number types)
    return df