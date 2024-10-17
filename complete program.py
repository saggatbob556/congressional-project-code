# barcode lookup license: "2zexfvl7jilokzgon5b3mwuldkfpjk"
# barcode license: "t0068lQAAAB1KwEW4syDLgyEan/ox1jzsKdrqymM+A97BgI1GKI1Qop/zgCpJH0778dkamsYYAGLZYZyCKQt9GokvNgnn1n0=;t0068lQAAAEwXD9bJmA7y1PU8CB3TUosceg1MJpVefKQTCIAMAHPBcMsI37bSEADLdaFe9zfyFNoGfo+o1jLUbWbnC3LJDn4="
#search URL: "https://ethical.org.au/search?q=doritos"
from __future__ import print_function
from bs4 import BeautifulSoup
import requests
from requests import ConnectionError
import numpy as np
import cv2 as cv 
from multiprocessing.pool import ThreadPool
from collections import deque  
import dbr
from dbr import *
import urllib.request
import json
import pprint


BarcodeReader.init_license("t0068lQAAAB1KwEW4syDLgyEan/ox1jzsKdrqymM+A97BgI1GKI1Qop/zgCpJH0778dkamsYYAGLZYZyCKQt9GokvNgnn1n0=;t0068lQAAAEwXD9bJmA7y1PU8CB3TUosceg1MJpVefKQTCIAMAHPBcMsI37bSEADLdaFe9zfyFNoGfo+o1jLUbWbnC3LJDn4=")
reader = BarcodeReader()

threadn = 1 # cv.getNumberOfCPUs()
pool = ThreadPool(processes = threadn)
barcodeTasks = deque()


def get_url(brand):
    if brand.lower() == "ge":
        brand = "General Electric"
    if brand.lower() == "pilot corporation":
        brand = "Pilot"
    if brand == "EXPO":
        brand = "newell brands"
    # Define the URL of the website to scrape
    url = "https://ethical.org.au/search?q=" + brand

    # Send an HTTP request to the website and retrieve the HTML content
    try:
        requests.get(url)
    except ConnectionError as e:
        return e
    response = requests.get(url)
        # Puts all html into soup
    soup = BeautifulSoup(response.content, 'html.parser')
    soup = str(soup.main())
    other_soup = BeautifulSoup(soup, 'html.parser')
    for company in other_soup.find_all("div", {"class", "mb-10"}):
        for link in company.find_all("a"):
            if (link.get_text()).lower() == brand.lower():
                return link.get("href")


def get_rating(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    soup_img = str(soup.find("div", {"class": "flex flex-col sm:flex-row items-center"}))
    soup_img = BeautifulSoup(soup_img, 'html.parser')
    soup_img = soup_img.find("img")
    soup_img = soup_img.get("alt")
    print("\nRating: " + soup_img)

    soup_praise = str(soup.find("div", {"class": "bg-assess-praise border border-assess-praise-dark px-2 md:block md:order-none order-2"}))
    soup_praise = BeautifulSoup(soup_praise, 'html.parser')
    print("\nPraise:")
    for praise in soup_praise.find_all("span", {"class": "leading-tight"}):
        print("-" + praise.get_text())

    soup_crit = str(soup.find("div", {"class": "bg-assess-criticism border border-assess-criticism-dark px-2 md:block md:order-none order-1"}))
    soup_crit = BeautifulSoup(soup_crit, 'html.parser')
    print("\nCriticisms:")
    for crit in soup_crit.find_all("span", {"class": "leading-tight"}):
        print("-" + crit.get_text())

    return "Done"


def process_frame(frame):
     results = None
     try:
         results = reader.decode_buffer(frame)
     except BarcodeReaderError as bre:
         print(bre)
        
     return results


def barcode_look(input):
    api_key = "2zexfvl7jilokzgon5b3mwuldkfpjk"
    url = "https://api.barcodelookup.com/v3/products?barcode=" + input + "&formatted=y&key=" + api_key

    with urllib.request.urlopen(url) as url:
        data = json.loads(url.read().decode())

    barcode = data["products"][0]["barcode_number"]
    print ("Barcode Number: ", barcode, "\n")

    name = data["products"][0]["title"]
    print ("Title: ", name, "\n")

    brand = data["products"][0]["brand"]
    print("Brand: " + brand)

    manufacturer = data["products"][0]["manufacturer"]
    print("Manufacturer: " + manufacturer)

    link = get_url(brand)
    link = get_url(manufacturer)
    print(link)
    if not link == None:
        print(get_rating(link))

    #print ("Entire Response:")
    #pprint.pprint(data)


vc = cv.VideoCapture(0)
while True:
     ret, frame = vc.read()
     while len(barcodeTasks) > 0 and barcodeTasks[0].ready():
         results = barcodeTasks.popleft().get()
         if results != None:
             for result in results:
                 points = result.localization_result.localization_points
                 cv.line(frame, points[0], points[1], (0,255,0), 2)
                 cv.line(frame, points[1], points[2], (0,255,0), 2)
                 cv.line(frame, points[2], points[3], (0,255,0), 2)
                 cv.line(frame, points[3], points[0], (0,255,0), 2)
                 cv.putText(frame, result.barcode_text, points[0], cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255))
                 barcode_look(result.barcode_text)

     if len(barcodeTasks) < threadn:
         task = pool.apply_async(process_frame, (frame.copy(), ))
         barcodeTasks.append(task)

     cv.imshow('Barcode & QR Code Scanner', frame)
     ch = cv.waitKey(1)
     if ch == 27:
         break
