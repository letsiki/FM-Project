import pytesseract
from PIL import Image, ImageEnhance, ImageFilter    

# Ensure the tesseract executable is in your PATH, or specify the location
# For example: pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\alexa\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    """
    Preprocess the image to improve OCR accuracy.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        Image: Preprocessed image.
    """
    img = Image.open(image_path)
    img = img.convert('L')  # Convert to grayscale
    img = img.filter(ImageFilter.SHARPEN)  # Apply sharpening filter
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(5)  # Increase contrast significantly
    return img

def extract_text_from_image(image_path):
    """
    Extract text from a given image using pytesseract.
    
    Args:
        image_path (str): The path to the image file.
    
    Returns:
        str: Extracted text from the image.
    """
    img = preprocess_image(image_path)
    text = pytesseract.image_to_string(img)
    return text

# List of image paths
image_paths = ['data/img/roles1of2.bmp', 'data/img/roles2of2.bmp']

# Extract text from each image and combine
combined_text = ""
for image_path in image_paths:
    text = extract_text_from_image(image_path)
    combined_text += text + "\n"  # Add a newline for separation between images

# Save the combined text to a file
output_file_path = 'roles.txt'
with open(output_file_path, 'w', encoding='utf-8') as file:
    file.write(combined_text)

print(f"Combined extracted text has been saved to {output_file_path}")