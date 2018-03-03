
import numpy as np
import cv2
import base64
import socket    
import queue
import io
import json

splitDelimiter="*****"
endingDelimiter="-----"
serverAddr='localhost'#'138.197.97.100'
serverPort=80
clientId=2434


def stringToReceive(str):
    splitAr=str.strip().split()
    rows=int(splitAr[1])
    cols=int(splitAr[2])
    #print(splitAr[3])
    decoded=base64.b64decode(splitAr[3][2:-1])
    #print(decoded)
    memfile = io.BytesIO()
    memfile.write(json.loads(decoded).encode('latin-1'))
    memfile.seek(0)
    a = np.load(memfile)
    #retAr=a.reshape(rows,cols)
    return (rows,cols,a)
    
    
def socketClient():

    s = socket.socket()         

    s.connect((serverAddr, serverPort))
    return s;


    
def receiveClient():

    q = queue.Queue()
    
    s=socketClient()
    wholeStr=""
    while(True):
        s.send(bytearray("recv \r\n",'utf-8'))
        #print("start")
        
        while( splitDelimiter not in wholeStr):
            wholeStr=wholeStr+s.recv(2048).decode('utf-8')
            
        splitStr=wholeStr.split(splitDelimiter)
        wholeStr=""
        for i in range(len(splitStr)):
            if endingDelimiter not in splitStr[i]:
                wholeStr=splitStr[i]
            else:
                q._put(splitStr[i])
                
                
        
        strRecv=q.get()
        #print(strRecv)
        #print("out")
        if(len(strRecv)==0):
            continue
        #print("done")
        rows,cols,frame=stringToReceive(strRecv)
        dim=(cols*1,rows*1)
        #resized = cv2.resize(frame, dim, interpolation = cv2.INTER_CUBIC)
        
        import numpy
        numpy.set_printoptions(threshold=numpy.nan)
        #print(frame)
        
        cv2.imshow("frameResized", frame)
        cv2.waitKey(1)
        

        
    
    

    
    # When everything done, release the capture
    
    cv2.destroyAllWindows()
    s.close()
receiveClient()
