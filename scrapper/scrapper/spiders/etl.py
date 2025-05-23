import pandas as pd #to clean transform and export information
import os
import sys

#Library csv cleanse
#Remove duplicates, change categories 'Default' and 'Add a comment' for 'Not specified'
#And split currency from price
def library_cleanse():
    current_dir = os.getcwd()
    export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
    library_df = pd.read_csv(os.path.join(export_dir, 'library.csv'), index_col=None, encoding= "utf-8")
    library_df1 = library_df.drop_duplicates(subset=['Title']).copy()
    library_df1.loc[(library_df1['Category'] == 'Add a comment') | (library_df1['Category'] == 'Default'),'Category'] = 'Not specified'
    library_df1.loc[:, 'Currency'] = library_df1['Price'].str.replace(" ", "", regex=False).str[0]
    library_df1.to_csv(os.path.join(export_dir, 'library.csv'), index=False)

#Book csv cleanse
#Merge library with books information, split currency from tax, price, and price with no tax
#And create the final excel (of raw data)
def book_cleanse():
    current_dir = os.getcwd()
    export_dir = os.path.join(current_dir, "scrapper", "spiders", "exports")
    books_df = pd.read_csv(os.path.join(export_dir, 'book_data.csv'), index_col=None, encoding= "utf-8")
    library_df = pd.read_csv(os.path.join(export_dir, 'library.csv'), index_col=None, encoding= "utf-8")
    merged_df = pd.merge(library_df, books_df, on='Title', how='inner')
    merged_df['Stock_quantity'] = merged_df['Stock_quantity'].str.extract(r'(\d+)').astype(int)
    merged_df.loc[:, 'Price_No_Tax'] = merged_df['Price_No_Tax'].str.slice(1).astype(float)
    merged_df.loc[:, 'Price_Tax'] = merged_df['Price_Tax'].str.slice(1).astype(float)
    merged_df.loc[:, 'Tax'] = merged_df['Tax'].str.slice(1).astype(float)
    result_df = merged_df[['UPC','Category','Title','Currency','Price_Tax', 'Price_No_Tax','Tax', 'Stock_availability', 'Stock_quantity', 'Rating','URL']]
    
    if os.path.exists(os.path.join(current_dir, 'result.csv')):
        old_result_file = pd.read_csv(os.path.join(current_dir, 'result.csv'), encoding= "utf-8")
        new_rows = result_df[~result_df['UPC'].isin(old_result_file['UPC'])]
        result_df = pd.concat([old_result_file, new_rows], ignore_index=True)

    result_df.to_csv(os.path.join(current_dir, 'result.csv'), index=False)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the function to run: 'library' or 'book'")
        sys.exit(1)

    task = sys.argv[1].lower()

    if task == "library":
        library_cleanse()
    elif task == "book":
        book_cleanse()
    else:
        print(f"Unknown task: {task}. Use 'library' or 'book'")
        sys.exit(1)
