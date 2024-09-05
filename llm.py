import openai
import scraping  #.py file for pasring and scraping the reviews

key=open("api_key_2.txt",'r').read()
openai.api_key = key

reviews = scraping.output['reviews']  #reviews from scarping file
#reviews = reviews[:10]
review_count = str(scraping.output['review_count'])  #num of reviews recieved/parsed

#print(review_count)

# Convert reviews to a single string, separated by new lines
formatted_reviews = "\n".join(reviews)

# Format the prompts as messages 
messages = [
    {"role": "system", "content": "You are a helpful assistant."},

    {"role": "user", "content": f"These are the {review_count} reviews from the app store for Lumosity:\n{formatted_reviews}\n\n"
                                "I want to use these reviews to come up with an onboarding form with rating questions, select/multi-select or a swipe layout to understand preferences so that we can personalize the experience. Also, the onboarding is as much about preferences as it is about education."},

    {"role": "user", "content": "ignore free users complaining about some premium features etc.Make questions more nuanced. "},

    {"role": "user", "content": "The initial question for a block can be rating questions on a scale of 1 to 5. The educational content can be presented as a series of 2-3 slides with images and H1/H2 text. Provide this as a JSON object, including question type, question text, and possible responses."}
]

def get_chat_response(messages, model="gpt-4o"):

    try:

        # Send the request to the OpenAI API
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )

        # Extract the content of the response
        return response.choices[0].message['content'].strip()
    
    except Exception as e:

        print(f"An error occurred: {e}")
        return None

# Get the response from the model
response_content = get_chat_response(messages)
print("Response from the model:")
print(response_content)

'''
messages=[{"role":"user", "content":"say hello world!"}]
response = openai.ChatCompletion.create(
    model="gpt-4",  # You can also use "gpt-3.5-turbo" for cheaper/quicker results
    messages=messages
)

print(response['choices'][0]['message']['content'])
'''