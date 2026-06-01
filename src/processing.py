import pandas as pd
from bs4 import BeautifulSoup
import re
def process_data(df: pd.DataFrame):
    required_cols = ['sku', 'name', 'short_description', 'description', 'categories', 'additional_attributes']
    df = df[required_cols]
    df.to_excel('data1.xlsx', index=False)  # Save the data inside of excel file with disabled numerical index (serial number types)
    return df

def extract_specifications(html_str: str) -> str:
    soup = BeautifulSoup(html_str, 'html.parser')
    specs_list = []
    for row in soup.find_all('tr'):
        th = row.find('th')
        td = row.find('td')
        if th and td:
            key = th.get_text(strip=True)
            value = td.get_text(strip=True)
            specs_list.append(f"{key}: {value}")

    specs_text = " | ".join(specs_list)

    specs_text = re.sub(r'\s+', ' ', specs_text).strip()

    return specs_text

def remove_category_with_po(df: pd.DataFrame):
    df = df[~df['categories'].str.lower().str.contains('po order')]
    return df