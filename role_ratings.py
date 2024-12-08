
import pandas as pd
import json
import os

def calculate_correlation_score(player_attributes, json_data):
    # Raw correlation score
    raw_score = 0
    max_possible_score = 0
    min_possible_score = 0
    
    for attribute, correlation in json_data.items():
        if attribute in player_attributes:
            attribute_value = player_attributes[attribute]
            # Calculate the raw correlation score
            raw_score += attribute_value * correlation
            
            # Determine the maximum and minimum possible scores for normalization
            if correlation > 0:
                max_possible_score += 20 * correlation
                min_possible_score += 1 * correlation
            else:
                max_possible_score += 1 * correlation
                min_possible_score += 20 * correlation

    # Normalize the score to a percentage
    if max_possible_score > min_possible_score:
        normalized_score = (raw_score - min_possible_score) / (max_possible_score - min_possible_score) * 100
    else:
        normalized_score = 0

    return min(max(normalized_score, 0), 100)

def process_player_correlations(df, json_folder_path):

    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]

    for index, row in df.iterrows():
        player_name = row.iloc[1]  # Assuming player name is in the first column
        player_attributes = row.iloc[4:].to_dict()  # Extracting attributes from column 4 to the end
        
        print(f'Player: {player_name}')
        
        for json_file in json_files:
            json_path = os.path.join(json_folder_path, json_file)
            
            with open(json_path, 'r') as file:
                json_data = json.load(file)
                # Drop Corners, Penalties, Free Kicks, Long Shots, Leadership
                attrs_to_remove = ['Pen', 'Fre', 'Cor', 'Ldr']
                for attr in attrs_to_remove:
                    del json_data['attr']
            
            correlation_percentage = calculate_correlation_score(player_attributes, json_data)
            json_file_name = os.path.splitext(json_file)[0]
            print(f'  JSON File: {json_file_name}, Total Correlation Percentage: {correlation_percentage:.2f}%')

def process_player_correlations_v2(df, json_folder_path):
    json_files = [f for f in os.listdir(json_folder_path) if f.endswith('.json')]
    
    for json_file in json_files:
        json_path = os.path.join(json_folder_path, json_file)
        json_file_name = os.path.splitext(json_file)[0]
        
        with open(json_path, 'r') as file:
            json_data = json.load(file)
        
        # Dictionary to store player names and their correlation percentages
        player_percentages = {}
        
        for index, row in df.iterrows():
            player_name = row.iloc[1]  # Assuming player name is in the first column
            player_attributes = row.iloc[4:].to_dict()  # Extracting attributes from column 4 to the end
            
            # Calculate the correlation percentage
            correlation_percentage = calculate_correlation_score(player_attributes, json_data)
            player_percentages[player_name] = correlation_percentage
        
        # Sort players by percentage in descending order
        sorted_players = sorted(player_percentages.items(), key=lambda item: item[1], reverse=True)
        
        # Print results
        print(f'JSON File: {json_file_name}')
        for player_name, percentage in sorted_players:
            print(f'  Player: {player_name}, Correlation Percentage: {percentage:.2f}%')

# Example usage:
df = pd.read_csv('FM Genie/1.csv')  # Load your DataFrame
process_player_correlations_v2(df, 'FM Genie/json/Low League')