# barcode license: "DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAzMjkwOTIzLVRYbFFjbTlxIiwibWFpblNlcnZlclVSTCI6Imh0dHBzOi8vbWRscy5keW5hbXNvZnRvbmxpbmUuY29tIiwib3JnYW5pemF0aW9uSUQiOiIxMDMyOTA5MjMiLCJzdGFuZGJ5U2VydmVyVVJMIjoiaHR0cHM6Ly9zZGxzLmR5bmFtc29mdG9ubGluZS5jb20iLCJjaGVja0NvZGUiOjE4NDc0MTg1Mjl9"
import numpy as np
import cv2 as cv
    
from multiprocessing.pool import ThreadPool
from collections import deque
    
import dbr
from dbr import *


BarcodeReader.init_license("DLS2eyJoYW5kc2hha2VDb2RlIjoiMTAzMjkwOTIzLVRYbFFjbTlxIiwibWFpblNlcnZlclVSTCI6Imh0dHBzOi8vbWRscy5keW5hbXNvZnRvbmxpbmUuY29tIiwib3JnYW5pemF0aW9uSUQiOiIxMDMyOTA5MjMiLCJzdGFuZGJ5U2VydmVyVVJMIjoiaHR0cHM6Ly9zZGxzLmR5bmFtc29mdG9ubGluZS5jb20iLCJjaGVja0NvZGUiOjE4NDc0MTg1Mjl9")
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

     if len(barcodeTasks) < threadn:
         task = pool.apply_async(process_frame, (frame.copy(), ))
         barcodeTasks.append(task)

     cv.imshow('Barcode & QR Code Scanner', frame)
     ch = cv.waitKey(1)
     if ch == 27:
         break
     