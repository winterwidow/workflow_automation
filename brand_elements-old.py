import pytesseract
import requests
from bs4 import BeautifulSoup
from PIL import Image
import re

#process the image and extract text from it

def extract_text_from_image(image_path):

    image = Image.open(image_path)
    # Perform OCR to get text from the image
    extracted_text = pytesseract.image_to_string(image)
    return extracted_text

#scrape CSS from the website and extract brand elements

def get_brand_elements_from_css(domain):

    # Get the HTML of the website
    html_response = requests.get(domain)
    soup = BeautifulSoup(html_response.text, 'html.parser')
    
    # Get all linked CSS files
    css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
    
    css_text = ""

    # Loop through all CSS files and extract their content

    for css_link in css_links:

        if not css_link.startswith('http'):
            css_link = domain + css_link
        css_response = requests.get(css_link)
        css_text += css_response.text
    
    #search for common brand elements in the CSS

    brand_elements = {
        'fonts': re.findall(r'font-family:\s*([^;]+);', css_text),
        'primary_color': re.findall(r'color:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgba?\([^)]+\));', css_text),
        'secondary_color': re.findall(r'background-color:\s*(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgba?\([^)]+\));', css_text),
        'background_image': re.findall(r'background-image:\s*url\(([^)]+)\);', css_text),
        'logo': re.findall(r'img.*src=["\']([^"\']+)["\']', html_response.text)  # Possible logo in img tags
    }
    
    return brand_elements

#orchestrate the extraction

def extract_brand_elements_from_image(image_path, domain):
    # Step 1: Extract text from the image (e.g., CSS class names, etc.)
    extracted_text = extract_text_from_image(image_path)
    
    # Step 2: Scrape and parse the website's CSS for brand elements
    brand_elements = get_brand_elements_from_css(domain)
    
    return {
        'extracted_text': extracted_text,
        'brand_elements': brand_elements
    }

#main

image_path = 'C:/Users/naija/Coding/onboarding/lumosity.png'  
domain = 'https://www.lumosity.com/en/'  #domain
result = extract_brand_elements_from_image(image_path, domain)

text= result['extracted_text']  #only text
elements = result['brand_elements'] #only brand elements

print(result, "\n")
print("text:\n", text)
print("elements:\n",elements)