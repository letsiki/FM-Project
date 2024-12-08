import pandas as pd
import json
import os
import sys

def calculate_role_value(attributes, weights):
    """
    Calculate role value based on player's attributes and role weights.
    
    Parameters:
    - attributes: A dictionary with player's attributes and their values.
    - weights: A dictionary with attribute weights for a role.
    
    Returns:
    - Role value for the player based on the weights.
    """
    # Convert attributes to numeric values, handling errors
    normalized_attributes = {}
    for k, v in attributes.items():
        try:
            value = float(v)
            if 1 <= value <= 20:  # Assuming attributes are within this range
                normalized_attributes[k] = (value - 1) / 19  # Normalize to range [0, 1]
        except ValueError:
            # Skip attributes that are not numeric
            pass
    
    # Normalize weights
    normalized_weights = {k: w for k, w in weights.items() if k in normalized_attributes}
    
    
    # Calculate the weighted sum
    weighted_sum = sum(normalized_attributes.get(k, 0) * normalized_weights[k] for k in normalized_weights)
    total_weight = sum(normalized_weights.values())
    
    # Normalize the score to be in the range [1, 20]
    if total_weight == 0:
        return 1  # Avoid division by zero if no weights are present

    role_value = (weighted_sum / total_weight) * 19 + 1  # Scale back to range [1, 20]
    
    return role_value

def evaluate_roles(df, json_dir='data/role_json'):
    """
    Evaluate roles for each player based on attributes and role weights.
    
    Parameters:
    - df: DataFrame containing player attributes.
    - json_dir: Directory where JSON files are located.
    
    Returns:
    - DataFrame with role values added.
    """
    # List JSON files in the directory
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    for json_file in json_files:
        role_name = os.path.splitext(json_file)[0]
        with open(os.path.join(json_dir, json_file), 'r') as f:
            weights = json.load(f)
        
        # Calculate role values for each player
        df[role_name] = df.apply(lambda row: calculate_role_value(row.to_dict(), weights), axis=1)
    
    return df

def print_row_details(df):
    """
    Iterate through each row in the DataFrame, print non-float64 entries,
    and print the 10 highest float64 values with their column names.
    
    Parameters:
    - df: pandas DataFrame with various data types
    """
    for index, row in df.iterrows():
        
        # Print non-float64 entries
        non_float64_entries = {col: val for col, val in row.items() if not pd.api.types.is_float_dtype(type(val))}
        for col, val in non_float64_entries.items():
            print(f"{col}: {val}")
        
        # Print top 30 highest float64 values
        float64_entries = {col: val for col, val in row.items() if pd.api.types.is_float_dtype(type(val))}
        top_50_float64 = sorted(float64_entries.items(), key=lambda x: x[1], reverse=True)[:50]

        # Filter rples that are are more than one point less suitable than the best role
        
        # Get the value of the first tuple
        first_value = top_50_float64[0][1]
    
        # Create a new list excluding tuples where the value is more than 1 lower than the first value
        filtered_list = [t for t in top_50_float64 if t[1] >= first_value - 1]

        print("\nTop 50 Roles:")
        for col, val in filtered_list:
            print(f"  {col}: {val}")
        print('\n')



# Open the file in write mode
ori_std_out = sys.stdout
file = open('output.txt', 'w') # change to 'a' for  append
sys.stdout = file
sys.stdout.reconfigure(encoding='utf-8')

# Example usage
df = pd.read_csv('evaluate_roles/csv/oostendeyoungsters.csv')
df_with_roles = evaluate_roles(df)

# Convert Useful Columns to strings prior to dropping all attributes
# df_with_roles['Vers'] = df_with_roles['Vers'].astype(str)
# df_with_roles['Cons'] = df_with_roles['Cons'].astype(str)
# df_with_roles['Inj Pr'] = df_with_roles['Inj Pr'].astype(str)
# df_with_roles['Imp M'] = df_with_roles['Imp M'].astype(str)
# df_with_roles['Det'] = df_with_roles['Det'].astype(str)
# df_with_roles['Prof'] = df_with_roles['Prof'].astype(str)
try:
    df_with_roles['Age'] = df_with_roles['Age'].astype('str')
except KeyError:
    pass

# Drop all attributes
df_with_roles = df_with_roles.drop(columns=df.select_dtypes(include=['int64']).columns)

# Round all float64 values to 2 decimal places
df_float64 = df_with_roles.select_dtypes(include=['float64'])
df_with_roles[df_float64.columns] = df_float64.round(2)
df_with_roles = df_with_roles.drop(columns=['Inf'])
try:
    df_with_roles = df_with_roles.drop(columns=['Position Selected']) 
except KeyError:
    pass
df_with_roles['Age'] = df_with_roles['Age'].astype(int)
# df_with_roles = df_with_roles.loc[df_with_roles['Age'] == 19]
# df_with_roles = df_with_roles.drop(columns=['Av Rat'])
# df_with_roles = df_with_roles.drop(columns=['Cont'])
print_row_details(df_with_roles)
sys.stdout = ori_std_out
file.close()


# df_with_roles.to_csv('evaluate_roles/csv/1withroles.csv', index=False)
