
import numpy as np
import cv2
import base64
import socket    
import io
import json

splitDelimiter="*****"
endingDelimiter="-----"
serverAddr='localhost'#'165.227.182.177'
serverPort=80
clientId=2434
def stringToSend(frame):

    memfile=io.BytesIO()
    np.save(memfile, frame)
    memfile.seek(0)
    serialized = json.dumps(memfile.read().decode('latin-1'))
    encoded = base64.b64encode(serialized.encode())
    rows=frame.shape[0]
    cols=frame.shape[1]
    #When sending from python 2.7 client use add "b'" and "'" around encoded
    #Code below will only work with python 3
    sentStr="send "+str(rows)+" "+str(cols)+" "+str(encoded)+" "+endingDelimiter+" "+splitDelimiter
    return sentStr


    
    
def socketClient():

    s = socket.socket()         

    s.connect((serverAddr, serverPort))
    return s;

def sendClient():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap.open()
    
    s=socketClient()
    iter=0
    while(True):
    # Capture frame-by-frame
        ret, frame = cap.read()
        iter+=1
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        s.send(bytearray(stringToSend(frame)+"\r\n",'utf-8'))

        

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    s.close()
    

sendClient()
