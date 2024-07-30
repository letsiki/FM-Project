from html_to_csv_converter import html_table_to_csv
from csv_merger_to_dataframe import load_and_merge_csv_files_to_df
from correlations import calculate_correlations
from import_export_dict_json import dict_to_file
from move_html_files import move_html_files

# Change the path to whatever the relative source of the html files is
directory_path = 'data/Archetypes/Penalty Saver GK'
csv_directory_path = directory_path + '/csv'
json_directory_path = directory_path + '/json/correlations.json'

move_html_files(directory_path)
html_table_to_csv(directory_path)

# html_table_to_csv(directory_path)
df = load_and_merge_csv_files_to_df(csv_directory_path, mode='percentage',)

# For Header Won Ratio - STC uncomment to remove last unecessary column
# df = df.iloc[:, :-1]
print(df.head())
# print(df.columns)
# print(df.shape)
dict_to_file(calculate_correlations(df, negative_stat=False), json_directory_path)

