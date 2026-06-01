# Assignment A1: 
## Create a proper github repo that cleans all the data present in the raw product export. Note - you should not use ChatGPT. Try to solve the assignment all yourself. You can refer to the documentation. 

## Acceptance Criteria - 
- First drop all the columns except sku, name, short_description, description, categories, additional_attributes. Converts to Excel format for processing. Name it data1.xlsx
- Filter products based on additional_attributes. Only keep the enabled products.
- Extract the specifications from the additional_attributes and clean HTML tags. Normalise whitespacing.
- Remove additional_attributes column and replace its name with specifications_text (for the product specifications part of point 3).
- Remove all the products that belong to the PO Order category. 
