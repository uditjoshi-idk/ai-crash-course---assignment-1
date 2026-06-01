import pandas as pd

#First drop all the columns except sku, name, short_description, description, categories, additional_attributes. Converts to Excel format for processing. Name it data1.xlsx

def load_data(path: str):
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    csv_path = 'export_catalog_product_20251006_105554.csv'
    data = load_data(csv_path)
    print(data.head())
