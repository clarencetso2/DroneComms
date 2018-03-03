import numpy as np
import cv2
import base64
import socket    
import io
import json
import sys


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    cap.open()
    

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    retval,encoded=cv2.imencode('.jpg',frame,(cv2.IMWRITE_JPEG_QUALITY,50))
    memfile=io.BytesIO()
    np.save(memfile, encoded)
    memfile.seek(0)
    print("Memfile size:   " + str(sys.getsizeof(memfile)/1024.0))
    print(frame.shape)
    print(frame.dtype)
    print("Only encoded size:   " + str(sys.getsizeof(encoded)/1024.0))
    #print(sys.getsizeof(gray)/1024.0)
    #print(encoded)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    out=cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    cv2.imshow("frameResized", out)
    cv2.waitKey(1)
        