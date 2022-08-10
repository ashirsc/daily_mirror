import cv2
from datetime import datetime

cap = cv2.VideoCapture(-1) # video capture source camera (Here webcam of laptop)

while(True):
    ret,frame = cap.read() # return a single frame in variable `frame`
    cv2.imshow('img1',frame) #display the captured image


    if cv2.waitKey(1) & 0xFF == ord('y' or 's'): #save on pressing 'y'
        now = datetime.now()
        fileName = 'data/captures/{}.png'.format(now.strftime("%m-%d-%yT%H-%M-%S"))
        print("captured " + fileName)
        cv2.imwrite(fileName,frame)

    if cv2.waitKey(1) & 0xFF == ord('e'): #save on pressing 'y'
        cv2.destroyAllWindows()
        break

cap.release()
