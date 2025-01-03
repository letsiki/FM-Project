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

def capture_screen(region=None, filename='data/img/screenshot.png'):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    print(f"Screenshot saved as {filename}")

def preprocess_image(image_path):
    img = Image.open(image_path)
    # img = img.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Apply sharpening filter
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(5)  # Increase contrast significantly
    img.save('data/img/preprocessed_screenshot.png')
    print(f"Image preprocessed and saved as preprocessed_screenshot.png")
    return img

def find_text_on_screen(text, region=None):
    capture_screen(region=region)
    img = preprocess_image('data/img/screenshot.png')
    
    # Perform OCR on the image with custom configurations
    custom_config = r'--oem 3 --psm 1'  # Adjust as needed for better accuracy
    ocr_result = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config)
    
    print("OCR Results:", ocr_result)
    
    # Debugging: Save the OCR results to the log file
    for i, word in enumerate(ocr_result['text']):
        print(f"Detected word: '{word}' at ({ocr_result['left'][i]}, {ocr_result['top'][i]})")

    # Iterate over each detected word and its bounding box
    for i, word in enumerate(ocr_result['text']):
        if text.lower() in word.lower():
            x = ocr_result['left'][i]
            y = ocr_result['top'][i]
            width = ocr_result['width'][i]
            height = ocr_result['height'][i]
            center_x = x + width // 2
            center_y = y + height // 2
            print(f"Text '{text}' found at ({center_x}, {center_y})")
            return (center_x, center_y)
    
    print(f"Text '{text}' not found.")
    return None

def click_on_text_in_window(text, offset_x = 0, offset_y=0):
    location = find_text_on_screen(text)
    if location:
        click_position = (location[0] + offset_x, location[1] + offset_y)
        print(f"Clicking on text '{text}' at {click_position}")
        pyautogui.moveTo(click_position)
        pyautogui.click()
        return click_position
    else:
        print(f"Text '{text}' not found for clicking.")
        return None

def iterate_dropdown_items(roles):
    # Loop to go through a fixed number of items
    for role in roles:
        pyautogui.moveTo(edit_search_position)
        pyautogui.click()
        time.sleep(0.2) 
        # click_position = (role_position[0], role_position[1])
        # print(f"Clicking at {click_position}")
        pyautogui.moveTo(role_position)
        pyautogui.click()
        time.sleep(1.5)  # Wait for the dropdown to open

        # Press Arrow Up and Enter to select an item
        pyautogui.press('up')
        pyautogui.press('enter')
        time.sleep(1.5)  # Wait for the action to complete

        # Optional: Perform additional actions here
        pyautogui.moveTo(ok_position)
        pyautogui.click()
        time.sleep(2)  # Adjust sleep time as needed for the action to complete
        perform_action_on_item(role)

def perform_action_on_item(role):
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
    
    # Click on Football Manager 2023
    pyautogui.click(COORD_FOOTBALL_MANAGER)
    time.sleep(0.2)
    
    # Press Up Arrow three times
    pyautogui.press('up', presses=3, interval=0.1)
    pyautogui.press('enter', presses=1, interval=0.1)
    time.sleep(0.2)

    # Double click on Python
    pyautogui.doubleClick(COORD_PYTHON)
    time.sleep(0.2)
    
    # Double click on Projects
    pyautogui.doubleClick(COORD_PROJECTS)
    time.sleep(0.2)
    
    # Double click on FM Project
    pyautogui.doubleClick(COORD_FM_PROJECT)
    time.sleep(0.2)
    
    # Double click on Data
    pyautogui.doubleClick(COORD_DATA)
    time.sleep(0.2)
    
    # Double click on Roles
    pyautogui.doubleClick(COORD_ROLES)
    time.sleep(0.2)
    
    # Double click on Untitled
    pyautogui.doubleClick(COORD_UNTITLED)
    time.sleep(0.2)
    
    # Type the role entry
    pyautogui.typewrite(role)
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
        iterate_dropdown_items(roles)
        # pyautogui.moveTo(COORD_PROJECTS)
    finally:
        cleanup_logging(log_file)