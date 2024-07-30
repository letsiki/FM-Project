"""
gui version of convert_merge_and_display.py. 

enhancements:
- creates csv and json folders if non-existent
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
            
            df = load_and_merge_csv_files_to_df(self.csv_directory_path, **kwargs)
            # print("DataFrame Head:")
            # print(df.head())
            print('\nDataframe Shape:')
            print(df.shape)
            print()
            
            correlations_dict = calculate_correlations(df, **kwargs2)
            dict_to_file(correlations_dict, self.json_directory_path)
            
            print(f"Correlations saved to {self.json_directory_path}")

        except Exception as e:
            print(f"An error occurred: {e}")

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