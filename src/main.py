import pandas as pd
from pathlib import Path
from processing import process_data, remove_category_with_po, extract_specifications
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

    filtered_data['specifications_text'] = filtered_data['additional_attributes'].apply(extract_specifications)
    print("Specifications extracted and added to the DataFrame.")
    
    print("Columns before dropping 'additional_attributes':")
    print(filtered_data.columns)

    filtered_data.drop('additional_attributes', axis=1, inplace=True)


    print("additional_attributes column has been dropped.")
    print(filtered_data.columns)

    print('Categories with po order')
    print(filtered_data[filtered_data['categories'].str.lower().str.contains('po order')])

    print("Removing categories with 'po order'")
    filtered_data = remove_category_with_po(filtered_data)
    print("Categories with 'po order' have been removed.")
    print(filtered_data[filtered_data['categories'].str.lower().str.contains('po order')])

    print("Saving into finalOutput.xlsx")
    filtered_data.to_excel('finalOutput.xlsx', index=False)