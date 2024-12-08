"""
gui version of convert_merge_and_display.py. 

enhancements:
- creates csv and json folders if non-existent

bugs:
- (SOLVED) When creating a new directory from the selecto folder dialog html files get moved
to initial dir and cannot be found by the functions that follow. The rest of the functions
Problem Break Down
Browse Folders only creates folders, it does not move the file. And the folders it creates
are correct whether I use the new folder option or not 
FIle gets moved when I browse folders although there is no code in browse folders to move the file
It seems that there is some code in move_html_files.py that runs the function. This occurs even though
I only importwed the function not the whole module
So I now fixed it by adding if __name__ == '__main__'. THe question is why does the problem occur only when I 
create a new folder.
I could not figure it out but I have tested it and it now works in both cases
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import shutil
from html_to_csv_converter import html_table_to_csv
from csv_merger_to_dataframe import load_and_merge_csv_files_to_df
from correlations import calculate_correlations
from import_export_dict_json import dict_to_file
from move_html_files import move_html_files
import matplotlib.pyplot as plt
import numpy as np

# Create the main application window
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("File Management GUI")
        self.directory_path = ""
        self.csv_directory_path = ""
        self.json_directory_path = ""

        # Browse Folders Button
        self.browse_button = tk.Button(root, text="Browse Folders", command=self.browse_folders)
        self.browse_button.pack(pady=10)

        # Checkboxes
        self.percentage_var = tk.BooleanVar()
        self.non_unique_ids_var = tk.BooleanVar()
        self.negative_stat_var = tk.BooleanVar()
        
        self.percentage_checkbox = tk.Checkbutton(root, text="Percentage", variable=self.percentage_var)
        self.non_unique_ids_checkbox = tk.Checkbutton(root, text="Non-Unique IDs", variable=self.non_unique_ids_var)
        self.negative_stat_checkbox = tk.Checkbutton(root, text="Negative Stat", variable=self.negative_stat_var)

        self.percentage_checkbox.pack()
        self.non_unique_ids_checkbox.pack()
        self.negative_stat_checkbox.pack()

        # Calculate Button
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate)
        self.calculate_button.pack(pady=10)

        # Text widget for output
        self.output_text = tk.Text(root, height=10, width=80)
        self.output_text.pack(expand=True, fill=tk.BOTH, pady=10)

        # Redirect stdout to the text widget
        self.output_stream = TextStream(self.output_text)
        sys.stdout = self.output_stream

        # # Print Warning
        # print('PLEASE DO NOT CHOOSE TO CREATE A NEW FOLDER FROM THE \'Browse Folders\' DIALOG!!!')

    def browse_folders(self):
        initial_dir = os.path.join(os.getcwd(), 'data')
        self.directory_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if self.directory_path:
            self.csv_directory_path = os.path.join(self.directory_path, 'csv')
            self.json_directory_path = os.path.join(self.directory_path, 'json', 'correlations.json')
            print(f"Selected Directory Path: {self.directory_path}")

        # Create self.csv_directory_path if it does not exist
        if not os.path.exists(self.csv_directory_path):
            os.makedirs(self.csv_directory_path, exist_ok=True)
            print(f"Created directory: {self.csv_directory_path}")

        # Create self.directory_path + 'json' if it does not exist
        json_dir = os.path.join(self.directory_path, 'json')
        if not os.path.exists(json_dir):
            os.makedirs(json_dir, exist_ok=True)
            print(f"Created directory: {json_dir}")

    def calculate(self):
        if not self.directory_path:
            messagebox.showwarning("Warning", "Please select a directory first.")
            return

        try:
            move_html_files(self.directory_path)
            html_table_to_csv(self.directory_path)  
            
            kwargs = {}
            kwargs2 = {}
            if self.percentage_var.get():
                kwargs['mode'] = 'percentage'
            if self.non_unique_ids_var.get():
                kwargs['unique_ids'] = False
            if self.negative_stat_var.get():
                kwargs2['negative_stat'] = True
            
            self.df = load_and_merge_csv_files_to_df(self.csv_directory_path, **kwargs)
            # print("DataFrame Head:")
            # print(df.head())
            print('\nDataframe Shape:')
            print(self.df.shape)
            print()
            
            self.correlations_dict = calculate_correlations(self.df, **kwargs2)
            dict_to_file(self.correlations_dict, self.json_directory_path)
            
            print(f"Correlations saved to {self.json_directory_path}")

        except Exception as e:
            print(f"An error occurred: {e}")
        # Uncheck to run plot()
        # self.plot()

    def plot(self):
        """
        Prints the plots of the five most important correlations
        """

        # Get the first 5 keys from the dictionary
        keys = list(self.correlations_dict.keys())[:5]

        for key in keys:
            # Check if the key exists in the DataFrame columns
            if key in self.df.columns:
                # Create a new DataFrame with two columns
                new_df = self.df[[key, self.df.columns[3]]].copy()

                  # Count the occurrences of each group
                group_counts = new_df[key].value_counts()  # New line

                # Filter groups with at least 150 occurrences
                valid_groups = group_counts[group_counts >= 40].index  # New line
            
                # Filter the new DataFrame to keep only valid groups
                new_df = new_df[new_df[key].isin(valid_groups)]  # Modified line
                
                # Group by the 'key' column and calculate the mean of 'fourth_column'
                new_df = new_df.groupby(key).agg({self.df.columns[3]: 'mean'}).reset_index()
                
                # Rename columns for clarity
                new_df.columns = [key, f'Average_{self.df.columns[3]}']
                
                # Plot the data
                plt.figure(figsize=(10, 6))
                plt.plot(new_df[key], new_df[f'Average_{self.df.columns[3]}'], marker='o', linestyle='-')
                plt.title(f'Average of {self.df.columns[3]} vs {key}')
                plt.xlabel(key)
                plt.ylabel(f'Average of {self.df.columns[3]}')

                # Set x-axis ticks to show integers from 1 to 20
                plt.xticks(np.arange(1, 21, 1))  # Use numpy to create an array from 1 to 20 with step 1

                plt.grid(True)
                plt.show()
            else:
                print(f"Column '{key}' not found in DataFrame.")

        

class TextStream:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(width=1100, height=900)
    app = App(root)
    root.mainloop()

# Plot code for using ranges instead of single values

    # def plot(self):
    #     # Define the bin edges and labels for grouping ranges
    #     bins = [0, 5, 10, 15, 20]
    #     labels = ['1-5', '6-10', '11-15', '16-20']

    #     # Get the first 5 keys from the dictionary
    #     keys = list(self.correlations_dict.keys())[:5]

    #     for key in keys:
    #         # Check if the key exists in the DataFrame columns
    #         if key in self.df.columns:
    #             # Create a new DataFrame with two columns
    #             new_df = self.df[[key, 'fourth_column']].copy()
                
    #             # Create a new column for range grouping
    #             new_df['Range'] = pd.cut(new_df[key], bins=bins, labels=labels, right=True)
                
    #             # Count the occurrences in each range
    #             range_counts = new_df['Range'].value_counts()
                
    #             # Filter ranges with at least 5 occurrences
    #             valid_ranges = range_counts[range_counts >= 5].index
                
    #             # Filter the new DataFrame to keep only valid ranges
    #             new_df = new_df[new_df['Range'].isin(valid_ranges)]
                
    #             # Group by the 'Range' column and calculate the mean of 'fourth_column'
    #             new_df = new_df.groupby('Range').agg({'fourth_column': 'mean'}).reset_index()
                
    #             # Rename columns for clarity
    #             new_df.columns = ['Range', 'Average_Fourth_Column']
                
    #             # Plot the data
    #             plt.figure(figsize=(10, 6))
    #             plt.plot(new_df['Range'], new_df['Average_Fourth_Column'], marker='o', linestyle='-')
    #             plt.title(f'Average of Fourth Column vs {key} (Grouped by Range)')
    #             plt.xlabel('Range')
    #             plt.ylabel('Average of Fourth Column')
                
    #             # Set x-axis ticks to show range labels
    #             plt.xticks(ticks=np.arange(len(labels)), labels=labels)
                
    #             plt.grid(True)
    #             plt.show()
    #         else:
    #             print(f"Column '{key}' not found in DataFrame.")