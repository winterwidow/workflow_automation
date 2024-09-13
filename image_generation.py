import openai
import json
#import llm
import requests
import re

key=open("api_key.txt",'r').read()
openai.api_key = key

def extract_json_object(response_text):
    # Identify the starting point of the JSON object
    start_idx = response_text.find('{')
    if start_idx == -1:
        print("No opening brace found.")
        return None
    
    stack = []
    json_str = ""
    
    for i in range(start_idx, len(response_text)):
        char = response_text[i]
        if char == '{':
            stack.append(char)
        elif char == '}':
            stack.pop()
        
        json_str += char
        
        if not stack:
            break
    
    if stack:
        print("Mismatched braces, no complete JSON object found.")
        return None
    
    return json_str

def load_json(filepath):

    print("Entered load_json function")  # debug

    # Read the JSON file
    try:
        with open(filepath, 'r') as file:
            content = file.read()
        #print(content)  # Debug: Print the full content

        # Parse the content to a Python dictionary
        data = json.loads(content)
        
        # Extract the "response" field
        response_text = data.get("response", "")
        
        # Extract the embedded JSON object within the "response" string
        embedded_json_str = extract_json_object(response_text)
        
        if embedded_json_str:
            # Parse the extracted JSON string to ensure it's valid JSON
            embedded_json = json.loads(embedded_json_str)
            
            # Store the extracted JSON object as a string (or return it as a dictionary)
            return json.dumps(embedded_json, indent=4)  # Returns as a pretty-printed JSON string
            
        else:
            print("No JSON object found in the 'response' field.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_data(content):


    print("entered extract_data function") #debug -- works

    '''try:
        # Step 1: Read the file content
        with open(filepath, 'r') as file:
            content = file.read()

        # Step 2: Use regex to find the JSON block within the text
        # Extract the JSON object inside the triple backticks
        json_match = re.search(r'```json\s*([\s\S]*?)```', content)
        
        if json_match:
            json_string = json_match.group(1).strip()
            
            # Clean up the JSON string
            json_string = json_string.replace('\\"', '"')  # Replace escaped quotes
            json_string = re.sub(r'\s+', ' ', json_string)  # Replace all whitespace (including newlines) with a single space
            json_string = json_string.strip()  # Remove any leading or trailing whitespace
            
            print(f"Extracted JSON string: {json_string}")  # Debugging output

            # Step 3: Load the JSON string into a Python object
            try:
                json_data = json.loads(json_string)
                return json_data
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                return None
        else:
            print("No JSON found in the response string.")
            return None'''
    
    try:
        # Find the positions of the first '{' and the last '}'
        json_start = content.find('{')
        json_end = content.rfind('}')

        if json_start != -1 and json_end != -1:
            json_str = content[json_start:json_end + 1]
            json_data = json.loads(json_str)
            print("Successfully extracted JSON!")  # Debugging line
            return json_data
        else:
            print("No JSON object found in the content.")
            return None

    except Exception as e:
        print(f"Error reading the file: {e}")
        return None

def generate_image(prompt):
    print("enetred generetae_image")#debug

    try:

        print(f"Calling OpenAI API with prompt: {prompt}") 
        
        # Call the DALL-E API to generate the image
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size
        )

        print(f"API response: {response}")  # Debugging line
        # Extract the image URL from the response
        image_url = response['data'][0]['url']

        print(f"Generated image URL: {image_url}")
        print(f"Generated image URL: {image_url}")
        return image_url

    except Exception as e:
        print(f"Error generating image: {e}")

def download_and_save_image(image_url, slide_id):
    try:
        response = requests.get(image_url)

        if response.status_code == 200:
            file_name = f"C:/Users/naija\AppData/Local/Programs/Python/Python310/Scripts/python progs/onboarding/onboarding/images/slide_{slide_id}.png"

            with open(file_name, 'wb') as file:  #filename needs to be written
                file.write(response.content)

            print(f"Image successfully saved as {file_name}")
            return file_name
        
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"An error occurred while downloading the image: {e}")
        return None

#main

#print("calling load_json function")  #debug
json_string= load_json('output_response.json')
#print("successfully executed load_json")  #debug
#print(json_string)

#print("calling extract_data function")  #debug -- works
json_response = extract_data(json_string)
#print("sucessfully executed extract_data fnction")#debug -- works

if json_response:
    print("Extracted JSON response:", json_response)  #debug -- works

    onboarding_form_list = json_response.get('onboarding_form', [])
    educational_slides = []

    # Iterate over the list to find the 'educational_content'
    for form_item in onboarding_form_list:
        if 'educational_content' in form_item:
            educational_slides = form_item['educational_content']
            break

    if educational_slides:
        print(f"Processing educational slides")  # Debugging line
        print(educational_slides)

        for slide in educational_slides:
            print("entered educational_slides for-loop")#debug

            header1 = slide.get('H1_text', '')
            header2 = slide.get('H2_text', '')j

            # Prompt for generating image
            add_info= "Make sure image conveys meaning behind the given header texts in the form of pictures."
            add_info2="No text in the images \n"
            prompt = f"{header1} - {header2}"

            message= f"{add_info}.{add_info2}.{prompt}"

            #print(f"Generating image with prompt: {prompt}")  # Debugging line
            print("calling generate_image function")#debug
            image_url = generate_image(message)
            print("sucessfully executed generate_image function")#debug

            if image_url:
                slide_id = slide.get('slide', 'unknown')
                saved_file_name = download_and_save_image(image_url, slide_id)

                if saved_file_name:
                    print(f"Generated and saved image for slide {slide_id}: {saved_file_name}")

                else:
                    print(f"Failed to save image for slide {slide_id}")
            else:
                print(f"Failed to generate image for slide {slide.get('slide', 'unknown')}")
            break
    else:
        print("Failed to find 'educational_content' in the onboarding form.")
else:
    print("Failed to extract and load the JSON response.")