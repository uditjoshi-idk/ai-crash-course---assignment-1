import pandas as pd
from pathlib import Path
from processing import process_data
from filtering import filter_data
PATH = Path(__file__).parent.parent

if __name__ == "__main__":

    csv_path = PATH / 'export_catalog_product_20251006_105554.csv'
    data = pd.read_csv(csv_path)

    print("Data loaded successfully.")
    print(data.head(), end = "\n\n")

    processed_data = process_data(data)
    print("Data has been processed and saved to data1.xlsx")
    print("loading data from data1.xlsx")

    data = pd.read_excel('data1.xlsx')
    print("Data loaded successfully.")
    print(data.head(), end = "\n\n")

    filtered_data = filter_data(data)
    print("Data has been filtered.")
    print(filtered_data.head(), end = "\n\n")
