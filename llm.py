import openai
import scraping

key=open("api_key",'r').read()
openai.api_key = key

reviews = scraping.output['reviews']
review_count = scraping.output['review_count']