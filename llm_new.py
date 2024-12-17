import openai
import json
import scraping  #.py file for pasring and scraping the reviews

key=open("api_key.txt",'r').read()
openai.api_key = key

reviews = scraping.output['reviews']  #reviews from scarping file
review_count = str(scraping.output['review_count'])  #num of reviews recieved/parsed

#convert reviews to a single string, separated by new lines
formatted_reviews = "\n".join(reviews)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},

    {"role": "user", "content": f"These are the {review_count} reviews from the app store for Lumosity:\n{formatted_reviews}\n\n"
                                "I want to use these reviews to create an onboarding form called `onboarding_form` with rating questions, select/multi-select options, or a swipe layout. The purpose of this form is to understand user preferences for a more personalized experience. Additionally, this onboarding should educate users on the app's offerings"},

    {"role": "user", "content": "ignore free users complaining about missing premium features. Make questions more nuanced to reflect deeper insights into user needs. We can structure it by asking a few preference questions, followed by educational content."},

    {"role": "user", "content": (
        "The first five questions should be rating questions on a scale of 1 to 5. For educational content, include three slides labeled as `educational_content`, each with `H1_text`, `H2_text`, and an image. The educational slides should highlight the app's key benefits."
        "Here’s an example format in JSON:\n\n"
        "{\n"
        "  \"onboarding_form\": [\n"
        "    {\n"
        "      \"question_type\": \"rating\",\n"
        "      \"question_text\": \"How would you rate your interest in improving memory skills?\",\n"
        "      \"responses\": [\n"
        "        \"1 - Not interested\",\n"
        "        \"2 - Slightly interested\",\n"
        "        \"3 - Moderately interested\",\n"
        "        \"4 - Very interested\",\n"
        "        \"5 - Extremely interested\"\n"
        "      ]\n"
        "    },\n"
        "    {\n"
        "      \"question_type\": \"rating\",\n"
        "      \"question_text\": \"How motivated are you to improve your attention span?\",\n"
        "      \"responses\": [\n"
        "        \"1 - Not motivated\",\n"
        "        \"2 - Slightly motivated\",\n"
        "        \"3 - Moderately motivated\",\n"
        "        \"4 - Very motivated\",\n"
        "        \"5 - Extremely motivated\"\n"
        "      ]\n"
        "    }\n"
        "  ],\n"
        "  \"educational_content\": [\n"
        "    {\n"
        "      \"H1_text\": \"Unlock Your Full Cognitive Potential\",\n"
        "      \"H2_text\": \"Discover games that enhance your memory, attention, and problem-solving skills.\",\n"
        "      \"image\": \"image1.jpg\"\n"
        "    },\n"
        "    {\n"
        "      \"H1_text\": \"Daily Workouts\",\n"
        "      \"H2_text\": \"Engage with a variety of cognitive exercises designed to challenge different aspects of your brain every day.\",\n"
        "      \"image\": \"image2.jpg\"\n"
        "    },\n"
        "    {\n"
        "      \"H1_text\": \"Track Your Progress\",\n"
        "      \"H2_text\": \"Access detailed reports and insights to monitor your improvement and stay motivated.\",\n"
        "      \"image\": \"image3.jpg\"\n"
        "    }\n"
        "  ]\n"
        "}"
    )}
]

def get_chat_response(messages, model="gpt-4o"):

    try:

        response = openai.chat.completions.create(
            model=model,
            messages=messages,
        )

        # Extract the content of the response
        return response.choices[0].message.content
    
    except Exception as e:

        print(f"An error occurred: {e}")
        return None

#get the response from the model
response_content = get_chat_response(messages)

if response_content:
    print("Response from the model:")
    print(response_content)

    #save the response content to a JSON file
    output_file_path = "output_response.json"
    with open(output_file_path, 'w') as json_file:
        json.dump({"response": response_content}, json_file, indent=4)
    
    print(f"Response saved to {output_file_path}")
else:
    print("Failed to get a response from the model.")