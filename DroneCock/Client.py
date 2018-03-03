
import numpy as np
import cv2
import base64
import socket    


serverAddr='192.168.0.32'
serverPort=8000
clientId=2434
def stringToSend(frame):
    encoded = base64.b64encode(frame)
    rows=frame.shape[0]
    cols=frame.shape[1]
    return "send "+str(rows)+" "+str(cols)+" "+str(encoded)

def stringToReceive(str):
    splitAr=str.split()
    rows=splitAr[1]
    cols=splitAr[2]
    decoded=base64.b64decode(splitAr[3])
    return (rows,cols,np.frombuffer(decoded, dtype=np.uint8).reshape(rows,cols))
    
    
def socketClient():

    s = socket.socket()         

    s.connect((serverAddr, serverPort))
    return s;

def sendClient():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        cap.open()
    
    s=socketClient()
    sent=0
    while(True):
    # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(len(bytes(stringToSend(gray))))
        #s.sendall(bytes(stringToSend(gray)+str(" \r\n")))
        if sent%10==0:
            print("sent "+str(sent))
        sent+=1

        

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    s.close()
    
def receiveClient():


    
    s=socketClient()
    
    while(True):
        s.send(b"recv")
        print("start")
        strRecv=s.recv(100000).decode()
        print(strRecv)
        print("done")
        rows,cols,frame=stringToReceive(strRecv)
        dim=(cols*3,rows*3)
        resized = cv2.resize(frame, dim, interpolation = cv2.INTER_LINEAR)
        cv2.imshow("frameResized", resized)

    
    


    # When everything done, release the capture

    cv2.destroyAllWindows()
    s.close()
sendClient()
