# barcode lookup license: "6hmoe9di29m98zs9uhm8r897tnfrcm"
# barcode license: "t0068lQAAAB1KwEW4syDLgyEan/ox1jzsKdrqymM+A97BgI1GKI1Qop/zgCpJH0778dkamsYYAGLZYZyCKQt9GokvNgnn1n0=;t0068lQAAAEwXD9bJmA7y1PU8CB3TUosceg1MJpVefKQTCIAMAHPBcMsI37bSEADLdaFe9zfyFNoGfo+o1jLUbWbnC3LJDn4="
from __future__ import print_function
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

def process_frame(frame):
     results = None
     try:
         results = reader.decode_buffer(frame)
     except BarcodeReaderError as bre:
         print(bre)
        
     return results

def barcode_look(input):
    api_key = "6hmoe9di29m98zs9uhm8r897tnfrcm"
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
     
