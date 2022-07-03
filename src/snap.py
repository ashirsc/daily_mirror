import sys
import signal
from gpiozero import Button, LED
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from datetime import datetime
import cv2
import numpy as np
import io
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection




class Snapper:
    pause = False

    TIME_INTERVAL = .5

    VERT_UPPER_LIMIT = 0.3
    VERT_LOWER_LIMIT = 0.6
    HORZ_RIGHT_LIMIT = 0.6
    HORZ_LEFT_LIMIT = 0.4

    HEIGHT, WIDTH = 240, 320

    # camera, image, red_led, button

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (self.WIDTH,self.HEIGHT)
        self.camera.framerate = 24
        self.camera.rotation = 180
        sleep(2)


        self.red_led = LED(17)
        self.button = Button(2)

        
        def signal_handler(sig, frame):
            print('Shutting down')
            self.camera.close()
            self.red_led.close()
            self.button.close()
            sys.exit(0)


        signal.signal(signal.SIGINT, signal_handler)

        print("Initialized snapper")


    def drawValidZone(self,img):

        height, width, z = img.shape
        lineColor = (0, 0, 255)

        pt1 = (int(round(width * self.HORZ_LEFT_LIMIT)),
               int(round(height * self.VERT_UPPER_LIMIT)))
        pt2 = (int(round(width * self.HORZ_RIGHT_LIMIT)),
               int(round(height * self.VERT_LOWER_LIMIT)))

        cv2.rectangle(img,
                      pt1, pt2,
                      lineColor,
                      3)

        return img



    def drawMidpoint(self,img, midpoint):
        return cv2.circle(img, midpoint, 3, (255, 0, 0), 3)



    def centered(self, x, y, height, width):

        x = x/width
        y = y/height

        if x < self.HORZ_LEFT_LIMIT or x > self.HORZ_RIGHT_LIMIT:
            return False
        if y < self.VERT_UPPER_LIMIT or y > self.VERT_LOWER_LIMIT:
            return False

        return True



    def getMidpoint(self, img):
        with mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5) as face_detection:
            results = face_detection.process(img)

            if results.detections == None:
                return None

            height, width, z = img.shape

            midpointX = 0
            midpointY = 0
            # for detection in results.detections:
            detection = results.detections[0]
            left_eye = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.LEFT_EYE)
            right_eye = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE)
            midpointX = ((left_eye.x + right_eye.x) / 2)
            midpointY = ((left_eye.y + right_eye.y) / 2)

            return (int(round(midpointX * width)), int(round(midpointY*height)))



    def ignore_button_press(self):
        print("no face in valid zone")



    def handle_button_press(self):

        self.pause = True
        for i in range(2):
            self.red_led.on()
            sleep(self.TIME_INTERVAL)
            self.red_led.off()
            sleep(self.TIME_INTERVAL)
        self.red_led.on()
        sleep(self.TIME_INTERVAL)
        self.red_led.off()

        now = datetime.now()
        fileName = 'data/captures/{}.jpg'.format(
            now.strftime("%m-%d-%yT%H-%M-%S"))

        image = np.empty((self.HEIGHT * self.WIDTH * 3), dtype=np.uint8)

        self.camera.capture(image, 'bgr')
        image = image.reshape((self.HEIGHT, self.WIDTH, 3))
        cv2.imwrite(fileName, image)

        print("snapped")
        self.pause = False



    def run(self):

        while True:
            if not self.pause:
                image = np.empty((self.HEIGHT * self.WIDTH * 3), dtype=np.uint8)
                self.camera.capture(image, 'bgr')
                image = image.reshape((self.HEIGHT, self.WIDTH, 3))

                cv2.imwrite("feed.jpg", image)

                midpoint = self.getMidpoint(image)
                if midpoint == None:
                    continue

                image = self.drawValidZone(image)
                image = self.drawMidpoint(image, midpoint)

                if self.centered(midpoint[0], midpoint[1], self.HEIGHT, self.WIDTH):
                    self.red_led.on()
                    self.button.when_activated = self.handle_button_press
                else:
                    self.red_led.off()
                    self.button.when_activated = self.ignore_button_press



snapper = Snapper()
snapper.run()
