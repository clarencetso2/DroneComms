
import numpy as np
import cv2
import base64
import socket    
import io
import json
from tkinter import *
import threading

splitDelimiter="*****"
endingDelimiter="-----"
serverAddr='192.241.131.131'
serverPort=80
clientId="thermal" #No spaces or this screws up also no split delimiter or ending delimiter
compression=95 #Number from 1-100 for compression for jpeg 1 being worst quality, low file size, 100 being best quality, high file size
videoStreamNumber=0 #0 is usually webcam 1 is usually lepton

def stringToSend(frame):
    retval,encoded=cv2.imencode('.jpg',frame,(cv2.IMWRITE_JPEG_QUALITY,compression))
    memfile=io.BytesIO()
    np.save(memfile, encoded)
    memfile.seek(0)
    #buf=memfile.getbuffer()
    #serialized = json.dumps(memfile.read().decode('latin-1'))
    
    #print("Memfile: " + str(sys.getsizeof(memfile)/1024.0))
    #print("Memfile2: " + str(sys.getsizeof(buf)/1024.0))
    #memfile2=io.BytesIO()
    #memfile2.write(buf)
    #print("Memfile3: " + str(sys.getsizeof(memfile2)/1024.0))
    #print("Serialized: " + str(sys.getsizeof(serialized)/1024.0))
    #encoded = base64.b64encode(serialized.encode())
    #print("Encoded: " + str(sys.getsizeof(encoded)/1024.0))
    
    rows=frame.shape[0]
    cols=frame.shape[1]
    #print(frame.shape)
    #When sending from python 2.7 client use add "b'" and "'" around encoded
    #Code below will only work with python 3
    sentStr="send "+str(clientId)+" "+str(rows)+" "+str(cols)+" "
    return (bytearray(sentStr,'utf-8'),memfile.getbuffer())


    
    
def socketClient():

    s = socket.socket()         

    s.connect((serverAddr, serverPort))
    return s;

def sendClient(w,v):
    global compression
    cap = cv2.VideoCapture(videoStreamNumber)
    if not cap.isOpened():
        cap.open()
    
    s=socketClient()
    iter=0

    
    while(True):
    # Capture frame-by-frame
        ret, frame = cap.read()
        iter+=1
        if v.get()=='2':
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        stringBytes,frameBytes=stringToSend(frame)
        
        stringBytesSize=len(stringBytes)#sys.getsizeof(stringBytes)
        frameBytesSize=len(frameBytes)
        #print(sys.getsizeof(stringBytes))
        #print(len(stringBytes))
        totalLenBytes=(stringBytesSize+frameBytesSize+8).to_bytes(4,byteorder='big')
        stringLenBytes=(stringBytesSize).to_bytes(4,byteorder='big')
        frameLenBytes=(frameBytesSize).to_bytes(4,byteorder='big')
        #print(stringBytesSize)
        #print("dasda: " + str(sys.getsizeof(frameLenBytes)))
        #print(sys.getsizeof(stringLenBytes))
        #print(sys.getsizeof(frameLenBytes))
        s.send(totalLenBytes)
        #print("Total" + str(totalLenBytes))
        s.send(stringLenBytes)
        #print("String " + str(stringLenBytes))
        #print(int.from_bytes(stringLenBytes, byteorder='big'))
        s.send(frameLenBytes)
        #print("Frame " + str(frameLenBytes))
        s.send(stringBytes)
        s.send(frameBytes)
        #print(str(stringBytesSize+frameBytesSize+8))
        #print(str(stringBytesSize))
        #print(str(frameBytesSize))
        compression=w.get()
        

       
        

    # When everything done, release the capture
    cap.release()
    #cv2.destroyAllWindows()
    s.close()
    
def tinker():
    master=Tk()
    master.title("Out Compression: "+str(clientId))
    master.minsize(400, 50)
    w = Scale(master, from_=1, to=100, length=350, orient=HORIZONTAL)
    
    w.set(compression)
    w.pack()
    MODES = [
        ("Color", "1"),
        ("Grayscale", "2"),
    ]

    v = StringVar()
    v.set("1") # initialize
    for text, mode in MODES:
        b = Radiobutton(master, text=text,
                        variable=v, value=mode)
        b.pack()
    t = threading.Thread(target=sendClient,args=(w, v))
    t.daemon = True
    t.start()
    mainloop()
tinker()