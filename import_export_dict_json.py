import json

def dict_to_file(dictionary, filename):
    """
    Writes a dictionary to a text file in JSON format.
    
    Parameters:
    - dictionary: The dictionary to be written to the file.
    - filename: The name of the file to which the dictionary will be written.
    """
    with open(filename, 'w') as file:
        json.dump(dictionary, file, indent=4)

def file_to_dict(filename):
    """
    Reads a dictionary from a text file in JSON format.
    
    Parameters:
    - filename: The name of the file from which the dictionary will be read.
    
    Returns:
    - The dictionary read from the file.
    """
    with open(filename, 'r') as file:
        return json.load(file)
