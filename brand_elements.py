import openai
import pyautogui  ##
from PIL import Image
import pytesseract
from collections import Counter
from io import BytesIO
import numpy as np
import json
import image_generation

pytesseract.pytesseract.tesseract_cmd = r'tesseract'

key = open("api_key.txt", 'r').read().strip()
openai.api_key = key

#take a screenshot
def take_screenshot():
    """Capture a screenshot and return it as a PIL Image."""
    screenshot = pyautogui.screenshot()
    return screenshot

#extract the text from the image
def extract_text_from_image(image):
    """Extract text with bounding box information from the image using pytesseract."""
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    extracted_text = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()

        if text:

            #capture text along with its bounding box size and position
            left = data['left'][i]
            top = data['top'][i]
            width = data['width'][i]
            height = data['height'][i]

            extracted_text.append({
                'text': text,
                'bounding_box': {'left': left, 'top': top, 'width': width, 'height': height}
            })

    return extracted_text

#extract the coloursz from the image
def extract_colours_from_image(image, num_colours=5):
    """Extract dominant colours from image."""
    image = image.resize((150, 150))  #faster processing if resized
    img_array = np.array(image)
    pixels = img_array.reshape((-1, 3))

    counter = Counter(map(tuple, pixels))
    most_common_colours = counter.most_common(num_colours)

    hex_colours = [{'colour': rgb_to_hex(colour), 'count': count} for colour, count in most_common_colours]

    return hex_colours

#convert colour in rgb foramt to hex colours
def rgb_to_hex(rgb):
    """Convert an RGB tuple to hex format."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

#get all brand elements together
def analyze_brand(image):
    """Main function to analyze the brand details from an image."""
    extracted_text = extract_text_from_image(image)
    dominant_colours = extract_colours_from_image(image)

    prompt = f"""
    Based on the following details extracted from the image, 
    please provide the brand's primary colour, secondary colour, font info(font type, colour), logo info(font type, colour), and button info(colour, font type) in JSON format.

    Extracted Text: {extracted_text}
    Extracted colours: {dominant_colours}
    Please use font_types as agthered from the web.
    Please provide the JSON output with keys: 'brand_info' (consisting of 'primary_colour', 'secondary_colour'), 'font', 'logo', and 'button'.
    """

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    output = response.choices[0].message.content

    #save the JSON in a file
    output_file_path = "brand_info.json"

    with open(output_file_path, 'w') as json_file:
        json_file.write(output)

    print(f"Brand information saved to {output_file_path}")
    return output

#main
if __name__ == "__main__":
    screenshot_image = take_screenshot()
    brand_info = analyze_brand(screenshot_image)
    print("Brand Information:\n", brand_info)
