def process_roles_file(input_file_path):
    """
    Process the roles file by stripping external whitespace, replacing internal whitespace with underscores,
    converting to lowercase, and saving into a reversed list.
    
    Args:
        input_file_path (str): The path to the input roles file.
        output_file_path (str): The path to the output file where the reversed list will be saved.
    """
    try:
        # Read the contents of the file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Process each line
        processed_lines = []
        for line in lines:
            processed_line = line.strip().replace(' ', '_').lower()
            processed_lines.append(processed_line)

        # Reverse the list
        processed_lines.reverse()

        return processed_lines

    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the input and output file paths
input_file_path = 'roles.txt'

# Call the function to process the file
print(process_roles_file(input_file_path))