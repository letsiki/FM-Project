# from csv_merger_to_dataframe import load_and_merge_csv_files_to_df
# from html_to_csv_converter import html_table_to_csv
from import_export_dict_json import file_to_dict, dict_to_file
import csv_merger_to_dataframe as merger

# The directory that will provide the correlations
directory_path = 'data/Av Rat/Roles/Advanced Forward'
json_directory_path = directory_path + '/json/correlations.json'

# Optional Manual Entry of Correlations
correlations = {
    "Cons": 0.38,
    "Dri": 0.22,
    "Ant": 0.19,
    "OtB": 0.17,
    "Fla": 0.16,
    "Cmp": 0.15,
    "Cro": 0.14,
    "Lon": 0.13,
    "Nat": 0.12,
    "Acc": 0.12,
    "Cor": 0.11,
    "Fin": 0.11,
    "Imp M": 0.11,
    "Pac": 0.10,
    "Prof": 0.10,
    "Pen": 0.10,
    "Cnt": 0.09,
    "Fre": 0.09,
    "L Th": 0.09,
    "Sta": 0.09,
    "Agi": 0.08,
    "Wor": 0.07,
    "Spor": 0.07,
    "Dec": 0.07,
    "Ecc": 0.06,
    "Ref": 0.05,
    "Temp": 0.04,
    "Tea": 0.04,
    "Tec": 0.04,
    "Vis": 0.04,
    "Vers": 0.03,
    "Inj Pr": 0.03,
    "Fir": 0.02,
    "Aer": 0.02,
    "Mar": 0.02,
    "Str": 0.01,
    "Jum": 0.01,
    "Pas": 0.01,
    "Ldr": 0.01,
    "Det": 0.01,
    "Amb": 0.00,
    "Com": 0.00,
    "Bra": -0.01,
    "Thr": -0.01,
    "TRO": -0.02,
    "Han": -0.02,
    "Hea": -0.02,
    "Bal": -0.02,
    "Tck": -0.03,
    "Pos": -0.03,
    "Cmd": -0.04,
    "Kic": -0.04,
    "Pun": -0.06,
    "Agg": -0.06,
    "Cont": -0.06,
    "1v1": -0.07,
    "Dirt": -0.13
}

# Retrieve correlations from json file
correlations = file_to_dict(json_directory_path)

# The directory that holds the html file(s) that we want to check against the correlation dictionary
directory_path = 'data/Datasets to apply  correlation to/low div england strikers'
csv_directory_path = directory_path + '/csv'
corr_directory_path = directory_path + '/corr/correlation_results.csv'

# Make sure the data starts with unique id the name and position followed by any rating then followed by the attributes
df = merger.load_and_merge_csv_files_to_df(csv_directory_path, mode='rating')

# Function to calculate the projected rating
def calculate_projected_rating(row, coeffs):
    total = 0
    count = 0
    for attr, coeff in coeffs.items():
        if attr in row:
            total += row[attr] * coeff
            count += 1
    return (total / count) * 10 if count > 0 else 0

# # Optionally Filter the Dataframe
# df = df[
#     df['Position'].str.contains('AM') & 
#     df['Position'].str.contains('[LR]') & 
#     ~df['Position'].str.contains('C')
# ]

# Apply the function to each row in the DataFrame
df['projected_rating'] = df.apply(lambda row: calculate_projected_rating(row, correlations), axis=1)
df = df.loc[:, ['Name', 'Position', 'projected_rating']].sort_values(by='projected_rating',
                                                                 ascending=False)

# Write Dataframe to a csv
with open(corr_directory_path, 'w', encoding='UTF8') as file:
    file.write(df.to_csv())

# TODO:
#   For some reason this only returns only one row of data. Fix it. Also consider the code below for help

# # Change the path to whatever the relative source of the html files is
# directory_path = 'data/Av Rat/Barnet'
# csv_directory_path = directory_path + '/csv'
# html_table_to_csv(directory_path)
# import os
# import pandas as pd
# # Iterate over all files in the specified folder
# for filename in os.listdir(csv_directory_path):
#     if filename.endswith('.csv'):
#         # Read each CSV file into a dataframe
#         df = pd.read_csv(os.path.join(csv_directory_path, filename), index_col=0)
# df['projected_rating'] = df.apply(lambda row: calculate_projected_rating(row, correlations), axis=1)
# print(df.loc[:,['Name', 'Av Rat', 'projected_rating']].sort_values(by='projected_rating', ascending=False))
# import matplotlib.pyplot as plt
# import seaborn as sns

# # # Plotting
# # plt.figure(figsize=(10, 6))
# # sns.scatterplot(x='Av Rat', y='projected_rating', data=df)
# # plt.title('Scatter Plot of Av Rat vs. Projected Rating')
# # plt.xlabel('Av Rat')
# # plt.ylabel('Projected Rating')
# # plt.grid(True)
# # plt.show()


# # Ensure the DataFrame is sorted by the index or another column to reflect a meaningful order
# # For demonstration purposes, assume 'attribute1' should be used for sorting
# df = df.sort_values(by='projected_rating')

# # Plotting the continuous line graph for Av Rat based on row order
# plt.figure(figsize=(10, 6))
# plt.plot(range(len(df)), df['Av Rat'], linestyle='-', color='b')  # No marker argument
# plt.title('Continuous Line Graph of Av Rat by Row Order')
# plt.xlabel('Row Index')
# plt.ylabel('Av Rat')
# plt.grid(True)
# plt.show()

# # Calculate the correlation
# correlation = df['Av Rat'].corr(df['projected_rating'])
# print(f"Correlation between Av Rat and Projected Rating: {correlation:.2f}")