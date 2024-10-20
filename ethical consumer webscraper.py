from bs4 import BeautifulSoup
import requests
import re

ratings = []
brands = []
tradingNames = []
criticisms = []
praise = []
urls = []
categoryNames = []
# Define the URL of the website to scrape
for j in range(430):
    url = 'https://ethical.org.au/categories/' + str(j)

    # Send an HTTP request to the website and retrieve the HTML content
    response = requests.get(url)
    # Puts all html into soup
    soup = BeautifulSoup(response.content, 'html.parser')
    pattern = re.compile("Shop Ethical", re.MULTILINE | re.DOTALL)
    #soup = soup.find("title", string=" - Shop Ethical")
    soup = re.findall(">.*?(?=Shop Ethical!<)", str(soup))
    pattern2 = re.compile("var products = ", re.MULTILINE | re.DOTALL)
    soup2 = BeautifulSoup(response.content, 'html.parser')
    soup2 = soup2.find("script", string=pattern2)
    for i in range(str(soup2).count("\"Feature1\":")):
        print(soup[0][1:-3])
    #pattern = re.compile("var products = ", re.MULTILINE | re.DOTALL)
    #soup = soup.find("script", string=pattern)
    #for company in re.findall("\"company\":\{\".*?(?=\{)", str(soup)):
    #    temp = str(re.findall("\"url\":\".*?(?=\")", str(company))[0])
    #    urls.append(temp[temp.index("https"):].replace("\/", "/"))
    #print(str(j) + " companies done")
#count = 0
#for url in urls:
#    response2 = requests.get(url)
#    soup2 = BeautifulSoup(response2.content, 'html.parser')
#    output = ""
#    for company in soup2.find_all("div", {"class": "bg-assess-criticism border border-assess-criticism-dark px-2 md:block md:order-none order-1"}):
#        for tight in re.findall("\"leading-tight\">.*?(?=\<)", str(company)):
#            output += tight[16:] + ", "
#    if len(output) == 0:
#        praise.append("none")
#    else:
#        praise.append(output[:-2])
#    count += 1
#    print(str(count) + " urls done")
#for p in praise:
#    print(p)
    """for rating in re.findall("\"Rating\":\".\"", str(soup)):
        ratings.append(rating[10:11])
    for brand in re.findall("\"Name1\":\".*?(?=\")", str(soup)):
        brands.append(brand[9:])
    for tradeName in re.findall("\"TradingName\":\".*?(?=\")", str(soup)):
        tradingNames.append(tradeName)
    print(j,  " urls done")
for i in range(len(brands)):
        print(brands[i])
for i in range(len(ratings)):
    print(ratings[i])"""
# puts only the table elements into a list
"""for company in soup.find_all({"div", {"class": "bg=assess-praise border border-assess-praise-dark px-2 md:block md:order-none order-2"}):
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
        """



