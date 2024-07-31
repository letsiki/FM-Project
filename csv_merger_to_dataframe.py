import pandas as pd
import os

def load_and_merge_csv_files_to_df(folder_path, mode='rating', unique_ids=True):
    """
    We need to set the whether the 'stat' is a 'rating' (default) or a 'percentage'. In addition 
    we need to set whether the dataset consists of unique player ids (default) or recurring 
    player ids. For example when we have printed an extra large page many times there will be
    unwanted duplicates. If on the other hand we want to combine different simulations of 
    the same dataset we want to set it to False to allow for recurring player UID's
    By the default view that last two columns must be dropped. In case you are dealing with a 
    different table view adjust the drop_col_end value 

    I decided to drop Nan Stat rows upon merging, and to remove Inf and Rec Columns in the merged dataframe
    I might opt to remove both upon merging in the future
    """
    # Initialize an empty list to hold dataframes
    dataframes = []

    # Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            # Read each CSV file into a dataframe
            
            df = pd.read_csv(os.path.join(folder_path, filename))
            print(f'{filename} initial size is {len(df)}')
            df.dropna(subset=[df.columns[3]])
            print(f'{filename} size after dropping is {len(df)}')
            # Append the dataframe to the list
            dataframes.append(df)

    # Concatenate all dataframes
    merged_df = pd.concat(dataframes, ignore_index=True)

    # Drop duplicate rows based on the first column (ID)
    if unique_ids:
        merged_df.drop_duplicates(subset=merged_df.columns[0], inplace=True)
    # print(merged_df.columns[0])

    # List of columns to remove
    columns_to_remove = ['Rec', 'Inf']

    # Remove columns if they exist
    result_df = merged_df.drop(columns=[col for col in columns_to_remove if col in merged_df.columns], errors='ignore')

    # Convert the 'Stat' column to numeric values, forcing errors to NaN and then dropping those rows
    if mode == 'percentage':
        result_df.iloc[:, 3] = result_df.iloc[:, 3].str.rstrip('%')
    result_df.iloc[:, 3] = pd.to_numeric(result_df.iloc[:, 3], errors='coerce')

    result_df.to_csv(folder_path[:-4] + '/merged_n_cleaned.csv')
    print('merged_n_cleaned.csv created')

    return result_df

# Example usage:
# result = load_and_merge_csv_files('/path/to/your/csv/folder')
# print(result)
