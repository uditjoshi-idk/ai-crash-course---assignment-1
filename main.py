import pandas as pd

#First drop all the columns except sku, name, short_description, description, categories, additional_attributes. Converts to Excel format for processing. Name it data1.xlsx

def load_data(path: str):
    df = pd.read_csv(path)
    return df

def process_data(df: pd.DataFrame):
    required_cols = ['sku', 'name', 'short_description', 'description', 'categories', 'additional_attributes']
    df = df[required_cols]
    df.to_excel('data1.xlsx', index=False)  # Save the data inside of excel file with disabled numerical index (serial number types)
    return df

if __name__ == "__main__":
    csv_path = 'export_catalog_product_20251006_105554.csv'
    data = load_data(csv_path)
    print("Data loaded successfully.")
    print(data.head(), end = "\n\n")
    processed_data = process_data(data)
    print("Data has been processed and saved to data1.xlsx")
    print(processed_data.head(), end = "\n\n")