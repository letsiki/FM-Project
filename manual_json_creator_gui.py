
import tkinter as tk
from tkinter import filedialog
import json

# Define the attributes for each column
columns = {
    "Technical": ["Cor", "Cro", "Dri", "Fin", "Fir", "Fre", "Hea", "Lon", "L Th", "Mar", "Pas", "Pen", "Tck", "Tec"],
    "Mental": ["Agg", "Ant", "Bra", "Cmp", "Cnt", "Dec", "Det", "Fla", "Ldr", "OtB", "Pos", "Tea", "Vis", "Wor"],
    "Physical": ["Acc", "Agi", "Bal", "Jum", "Nat", "Pac", "Sta", "Str"],
    "GK": ["Aer", "Cmd", "Com", "Ecc", "Han", "Kic", "1v1", "Ref", "TRO", "Pun", "Thr"],
    "Hidden": ["Ada", "Amb", "Cons", "Cont", "Imp M", "Inj Pr", "Pres", "Prof", "Spor", "Temp", "Vers"]
}

class FootballManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Football Manager Attributes")

        self.primary_vars = {}
        self.secondary_vars = {}

        # Create frames for layout
        self.create_frames()

        # Add widgets to frames
        self.add_widgets()

    def create_frames(self):
        # Define frames for each column
        self.frame1 = tk.Frame(self.root)
        self.frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame2 = tk.Frame(self.root)
        self.frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frame3 = tk.Frame(self.root)
        self.frame3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.frame4 = tk.Frame(self.root)
        self.frame4.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.frame5 = tk.Frame(self.root)
        self.frame5.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky="ew")

    def add_widgets(self):
        # Create headers for columns
        tk.Label(self.frame1, text="Technical").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame1, text="P").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame1, text="S").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.frame2, text="Mental").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame2, text="P").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame2, text="S").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.frame3, text="Physical").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame3, text="P").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame3, text="S").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.frame4, text="GK").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame4, text="P").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame4, text="S").grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.frame5, text="Hidden").grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.frame5, text="P").grid(row=0, column=1, padx=5, pady=5)
        tk.Label(self.frame5, text="S").grid(row=0, column=2, padx=5, pady=5)

        # Add attributes and checkboxes to frames
        self.add_attributes(self.frame1, columns["Technical"])
        self.add_attributes(self.frame2, columns["Mental"])
        self.add_attributes(self.frame3, columns["Physical"])
        self.add_attributes(self.frame4, columns["GK"])
        self.add_attributes(self.frame5, columns["Hidden"])

        # Add save, reset, and load functionality
        self.save_entry = tk.Entry(self.bottom_frame, width=40)
        self.save_entry.grid(row=0, column=0, padx=5, pady=5)

        self.save_button = tk.Button(self.bottom_frame, text="Save", command=self.save_file)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)

        self.reset_button = tk.Button(self.bottom_frame, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2, padx=5, pady=5)

        self.load_button = tk.Button(self.bottom_frame, text="Load", command=self.load_file)
        self.load_button.grid(row=0, column=3, padx=5, pady=5)

    def add_attributes(self, frame, attribute_list):
        row = 1
        for attr in attribute_list:
            # Create variables for primary and secondary checkboxes
            primary_var = tk.BooleanVar()
            secondary_var = tk.BooleanVar()
            self.primary_vars[attr] = primary_var
            self.secondary_vars[attr] = secondary_var
            
            # Create and place labels and checkboxes
            tk.Label(frame, text=attr).grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            # Create primary and secondary checkbuttons with command bindings
            primary_cb = tk.Checkbutton(
                frame, variable=primary_var,
                command=lambda p=primary_var, s=secondary_var: self.toggle_check(p, s)
            )
            primary_cb.grid(row=row, column=1, sticky="w")
            
            secondary_cb = tk.Checkbutton(
                frame, variable=secondary_var,
                command=lambda s=secondary_var, p=primary_var: self.toggle_check(s, p)
            )
            secondary_cb.grid(row=row, column=2, sticky="w")
            
            row += 1

    def create_var(self, attribute, attr_type):
        var = tk.BooleanVar()
        return var

    def toggle_check(self, checked_var, unchecked_var):
        if checked_var.get():
            unchecked_var.set(False)

    def save_file(self):
        filename = self.save_entry.get().strip()
        if filename:
            filepath = f"{folder}{filename}.json"
            data = {}
            for attr, var in self.primary_vars.items():
                if var.get():
                    data[attr] = 1
            for attr, var in self.secondary_vars.items():
                if var.get():
                    data[attr] = 0.5
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"File saved as {filepath}")

    def reset(self):
        # Uncheck all checkboxes
        for var in self.primary_vars.values():
            var.set(False)
        for var in self.secondary_vars.values():
            var.set(False)
        
        # Clear the filename entry
        self.save_entry.delete(0, tk.END)

    def load_file(self):
        # Open file dialog to select a JSON file
        filepath = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            initialdir=folder
        )
        if filepath:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Extract filename without extension for the entry field
            filename = filepath.split('/')[-1].replace('.json', '')
            self.save_entry.delete(0, tk.END)
            self.save_entry.insert(0, filename)
            
            # Update checkboxes based on JSON data
            for attr in self.primary_vars:
                if attr in data:
                    if data[attr] == 1:
                        self.primary_vars[attr].set(True)
                        self.secondary_vars[attr].set(False)
                    elif data[attr] == 0.5:
                        self.primary_vars[attr].set(False)
                        self.secondary_vars[attr].set(True)
                else:
                    self.primary_vars[attr].set(False)
                    self.secondary_vars[attr].set(False)

# Create and run the application
folder = 'data/role_json/gegen/'
root = tk.Tk()
app = FootballManagerApp(root)
root.mainloop()

