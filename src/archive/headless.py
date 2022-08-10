import cv2
import time

cam = cv2.VideoCapture(3)

# cv2.namedWindow("test")

img_counter = 0
prev_frame_time = 0
new_frame_time = 0
font = cv2.FONT_HERSHEY_SIMPLEX

print("starting loop")
while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break

    new_frame_time = time.time()
 
    fps = 1/(new_frame_time-prev_frame_time)
    prev_frame_time = new_frame_time
    fps = int(fps)
    fps = str(fps)


    cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    img_name = "tmp/opencv_frame.png".format(img_counter)
    cv2.imwrite(img_name, frame)
    time.sleep()

    

cam.release()

