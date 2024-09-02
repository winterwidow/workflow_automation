import requests
#beautiful soup - parsing html & xml module
#https://pypi.org/project/beautifulsoup4/
from bs4 import BeautifulSoup

def scrape_reviews(url):

    #url finder
    locator=requests.get(url)

    #if request is succesful
    if(locator.status_code == 200):
        soup= BeautifulSoup(locator.content, 'html.parser') #stores the reviews

        reviews=[]

        #to scrape the reviews:
        for review in soup.find_all('div', class_='h3YV2d'):
            
                # Extract review text
                review_text = review.text.strip()
                reviews.append(review_text)  #store each review in the list

        return reviews
    else:
         print("failed to find reviews")
         return []
    
#main

url="https://play.google.com/store/apps/details?id=com.lumoslabs.lumosity&hl=en_IN"
reviews = scrape_reviews(url)

'''for review in reviews:
     print(review)'''
#print(len(reviews)) #3