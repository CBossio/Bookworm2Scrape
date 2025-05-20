import pandas as pd #to clean transform and export information
import os

#Library csv cleanse
def library_cleanse():
    current_dir = os.getcwd()
    export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
    library_df = pd.read_csv(os.path.join(export_dir, 'library.csv'), index_col=None)
    library_df1 = library_df.drop_duplicates(subset=['Title']).copy()
    library_df1.loc[(library_df1['Category'] == 'Add a comment') | (library_df1['Category'] == 'Default'),'Category'] = 'Not specified'
    library_df1.loc[:, 'Currency'] = library_df1['Price'].str.replace(" ", "", regex=False).str[0]
    library_df1.to_excel(os.path.join(export_dir, 'library.xlsx'), index=False)

#Book csv cleanse
def book_cleanse():
    current_dir = os.getcwd()
    export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
    books_df = pd.read_csv(os.path.join(export_dir, 'book_data.csv'), index_col=None)
    library_df = pd.read_excel(os.path.join(export_dir, 'library.xlsx'), index_col=None)
    merged_df = pd.merge(library_df, books_df, on='Title', how='inner')
    merged_df['Stock_quantity'] = merged_df['Stock_quantity'].str.extract(r'(\d+)').astype(int)
    merged_df.loc[:, 'Price_No_Tax'] = merged_df['Price_No_Tax'].str.slice(1).astype(float)
    merged_df.loc[:, 'Price_Tax'] = merged_df['Price_Tax'].str.slice(1).astype(float)
    merged_df.loc[:, 'Tax'] = merged_df['Tax'].str.slice(1).astype(float)
    result_df = merged_df[['UPC','Category','Title','Currency','Price_Tax', 'Price_No_Tax','Tax', 'Stock_availability', 'Stock_quantity','URL']]
    result_df.to_excel(os.path.join(current_dir, 'result.xlsx'), index=False)

