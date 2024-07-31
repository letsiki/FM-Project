import os
import shutil

def move_html_files(dest_relative_path):
    """
    Moves all HTML files from a fixed source directory to a destination directory
    specified by a relative path from the current working directory.
    
    :param dest_relative_path: Relative path to the destination directory.
    """
    print('move_html_files called')
    # Fixed source directory
    source_dir = r"E:\Documents\Sports Interactive\Football Manager 2023"
    
    # Convert relative destination path to absolute path
    dest_dir = os.path.abspath(dest_relative_path)
    
    # Ensure the source directory exists
    if not os.path.isdir(source_dir):
        raise ValueError(f"Source directory '{source_dir}' does not exist.")
    
    # Ensure the destination directory exists, create it if not
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)
    
    # List all files in the source directory
    files = os.listdir(source_dir)
    
    # Filter HTML files
    html_files = [f for f in files if f.lower().endswith('.html')]
    
    # Move each HTML file to the destination directory
    for html_file in html_files:
        src_path = os.path.join(source_dir, html_file)
        dest_path = os.path.join(dest_dir, html_file)
        
        # Move the file
        shutil.move(src_path, dest_path)
        print(f"Moved: {src_path} -> {dest_path}")

if __name__ == "__main__":
    # Example usage
    relative_destination = ""  # Relative path from current working directory
    move_html_files(relative_destination)
