
import numpy as np
import cv2

cap = cv2.VideoCapture(1)
#if not cap.isOpened():
#    cap.open()
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #edges = cv2.Canny(frame,50,100)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(frame.shape)
    # Display the resulting frame
    dim=(600,450)
    dim=(450,600)
    print(frame.shape)
    resized = cv2.resize(frame, dim, interpolation = cv2.INTER_LINEAR)
    
    cv2.imshow("frameResized", resized)
    #cv2.imshow("faa",frame)
    #cv2.imshow('edges',edges)
    #cv2.imshow('gray',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

