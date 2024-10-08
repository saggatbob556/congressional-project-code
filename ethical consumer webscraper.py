from bs4 import BeautifulSoup
import requests



# Define the URL of the website to scrape
url = 'https://www.ethicalconsumer.org/food-drink/shopping-guide/soft-drinks'

# Send an HTTP request to the website and retrieve the HTML content
response = requests.get(url)

# Puts all html into soup
soup = BeautifulSoup(response.content, 'html.parser')



# puts only the table elements into a list
for company in soup.find_all({"tr": "data-category-scores"}):
    if company.find("div", {"class": "product-company"}):
        temp = company.find('h4')
        print(temp.get_text())
        if company.find("div", {"class": "score good"}):
            temp2 = company.find("div", {"class": "score good"})
            print(temp2.get_text())
        else:
            if company.find("div", {"class": "score average"}):
                temp2 = company.find("div", {"class": "score average"})
                print(temp2.get_text())
            else:
                temp2 = company.find("div", {"class": "score bad"})
                print(temp2.get_text())
        



