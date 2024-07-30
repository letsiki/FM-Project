import pyautogui
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
import pygetwindow as gw
import sys
import roles_txt_to_list

# Placeholder coordinates (to be replaced with actual coordinates)
COORD_OK_BUTTON = (1050, 610)
COORD_FOOTBALL_MANAGER = (850, 420)
COORD_PYTHON = (750, 660)
COORD_PROJECTS = (750, 490)
COORD_FM_PROJECT = (750, 490)
COORD_DATA = (735, 530)
COORD_ROLES = (735, 490)
COORD_UNTITLED = (960, 340)
COORD_SAVE_BUTTON = (1150, 755)

# Get hold of the list of roles
roles = roles_txt_to_list.process_roles_file('roles.txt')

# Ensure the tesseract executable is in your PATH, or specify the location
# For example: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\alexa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

# Open a log file to capture all output
log_file_path = 'debug_log.txt'

def setup_logging():
    """ Set up logging to file """
    log_file = open(log_file_path, 'w')
    sys.stdout = log_file
    sys.stderr = log_file
    return log_file

def cleanup_logging(log_file):
    """ Clean up logging by closing the file handles """
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    log_file.close()
    print(f"Debug log saved as {log_file_path}")

def bring_window_to_focus(window_title):
    app_window = None
    for window in gw.getWindowsWithTitle(window_title):
        if window_title in window.title:
            app_window = window
            break

    if app_window:
        app_window.activate()
        time.sleep(1)  # Wait for the window to be brought into focus
        print(f"Window '{window_title}' activated.")
    else:
        print(f"Window with title '{window_title}' not found.")

def iterate_dropdown_items(iterations):
    # Loop to go through a fixed number of items
    perform_action_on_item()
    for i in range(iterations):
        pyautogui.moveTo(edit_search_position)
        pyautogui.click()
        time.sleep(0.2)
        # click_position = (role_position[0], role_position[1])
        # print(f"Clicking at {click_position}")
        pyautogui.moveTo(1600, 625)
        time.sleep(0.2)
        pyautogui.scroll(-120)
        time.sleep(1.2)
        # Optional: Perform additional actions here
        pyautogui.moveTo(ok_position)
        pyautogui.click()
        time.sleep(2)  # Adjust sleep time as needed for the action to complete
        perform_action_on_item(i)

def perform_action_on_item(i=-1):
    """
    This function will press control P then click ok then click on Fottball Manager 2023 the press up arrow three times
    then doubleclick python then double click projects  then double click on FM project then double click on data then 
    double click on roles then double click on Untitled then type the next entry from roles list then cick save
    """
    
    # Press Control + P
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(0.2)  # Sleep to allow action to complete
    
    # Click OK button
    pyautogui.click(COORD_OK_BUTTON)
    time.sleep(0.2)
    
    # Double click on Untitled
    pyautogui.doubleClick(COORD_UNTITLED)
    time.sleep(0.2)
    
    # Type the role entry
    pyautogui.typewrite(str(i))
    time.sleep(0.2)
    
    # Click Save button
    pyautogui.click(COORD_SAVE_BUTTON)
    time.sleep(0.2)

# Main script execution
if __name__ == "__main__":
    log_file = setup_logging()
    try:
        print("Starting actions in 3 seconds...")
        time.sleep(3)
        
        bring_window_to_focus("Football Manager 2023")
        edit_search_position = (1800, 250)
        ok_position = (1800, 740)
        role_position = (1250, 405)
        iterate_dropdown_items(24)
        # pyautogui.moveTo(1600, 625)
    finally:
        cleanup_logging(log_file)