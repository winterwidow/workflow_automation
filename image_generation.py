import openai
import json
import llm
import requests
import re

key=open("api_key.txt",'r').read()
openai.api_key = key

def extract_json_object(response_text):

    #identify the starting point of the JSON object
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

        data = json.loads(content)
        
        #extract the "response" field
        response_text = data.get("response", "")
        
        #extract the embedded JSON object within the "response" string
        embedded_json_str = extract_json_object(response_text)
        
        '''if embedded_json_str:
            #check validity of json
            embedded_json = json.loads(embedded_json_str)
            
            #store the extracted JSON object as a string (or return it as a dictionary)
            return json.dumps(embedded_json, indent=4)  '''
        
        if embedded_json_str:
            return json.loads(embedded_json_str)  #parses to a dictionary not string
            
        else:
            print("No JSON object found in the 'response' field.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def extract_data(content):
    
    try:
        # Find the positions of the first '{' and the last '}'
        json_start = content.find('{')
        json_end = content.rfind('}')

        if json_start != -1 and json_end != -1:
            json_str = content[json_start:json_end + 1]
            json_data = json.loads(json_str)
            print("Successfully extracted JSON!")  #debugging line
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
        
        response = openai.Image.create(
            prompt=prompt,
            n=1,  # Number of images to generate
            size="1024x1024"  # Image size
        )

        print(f"API response: {response}")  #debugging line
        #extract the image URL from the response
        image_url = response['data'][0]['url']

        print(f"Generated image URL: {image_url}")
        print(f"Generated image URL: {image_url}")
        return image_url

    except Exception as e:
        print(f"Error generating image: {e}")

def download_and_save_image(image_url, slide_id):
    #need to save it back into json output
    try:
        response = requests.get(image_url)

        if response.status_code == 200:
            #file_name = f"C:/Users/naija/AppData/Local/Programs/Python/Python310/Scripts/python progs/onboarding/onboarding/images/slide_{slide_id}.png" #change according to system

            file_name = f"/images/slide_{slide_id}.png" #change according to system

            with open(file_name, 'wb') as file:  
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

'''json_string= load_json('output_response.json')

json_response = extract_data(json_string)

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
            header2 = slide.get('H2_text', '')

            # Prompt for generating image
            add_info= "Images should match the meaning of the headers."
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
            #break
    else:
        print("Failed to find 'educational_content' in the onboarding form.")
else:
    print("Failed to extract and load the JSON response.")
'''

json_data=load_json('output_response.json') #json with data
#json data storing as dict

if json_data:
    print("extracted json response: ",json_data)

    # Extract 'onboarding_form' and 'educational_content' directly from json_response
    onboarding_form_list = json_data.get('onboarding_form', [])
    educational_slides = json_data.get('educational_content', [])

    # Check if educational_slides was successfully extracted
    if educational_slides:
        print("Educational Slides:", educational_slides)
    else:
        print("No educational content found.")

    #each slide in educational content
    if educational_slides:
        
        for slide in educational_slides:
            header1=slide.get('H1_text','')
            header2=slide.get('H2_text','')

            add_info= "Images should match the meaning of the headers."
            add_info2="No text in the images \n"
            prompt = f"{header1} - {header2}"
            message= f"{add_info}.{add_info2}.{prompt}"

            print()
            print(f"Generating image with prompt: {prompt}")  #debugging line
            print("calling generate_image function")#debug
            image_url = generate_image(message)
            print("sucessfully executed generate_image function") #debug

            if image_url:
                slide['generated_image_url']=image_url
                print(f"added generated image url for slide {slide.get('slide','unknown')}")

        #save to new json
        with open('updated_output_response.json','w')as file:
            json.dump(json_data,file, indent=4)
        print('updated response saved to json')
    else:
        print("Failed to find 'educational_content' in the json file")
else:
    print("failed to extract and load the json data")

print("\n UPDATED JSON:\n\n\n")
print("Updated JSON:\n", json.dumps(json_data, indent=4))

            