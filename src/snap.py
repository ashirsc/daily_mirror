
import sys
import signal
from gpiozero import Button, LED
from time import sleep
from datetime import datetime
import cv2

from identify import load_encodings, get_image_face_ids, save_new_faces




class Snapper:

    TIME_INTERVAL = .5
    HEIGHT, WIDTH = 240*2, 320*2

    ENCODING_DIR = "data/encodings"


    def __del__(self):
        self.cam.release()

    def __init__(self):
        self.known_faces = load_encodings(self.ENCODING_DIR)
        self.cam = cv2.VideoCapture(3)

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

  
    def ignore_button_press(self):
        print("no face in valid zone")

    def blink(self, intervals, duration):
        for i in range(intervals):
            self.red_led.on()
            sleep(duration)
            self.red_led.off()
            sleep(duration)
        self.red_led.on()
        sleep(duration)
        self.red_led.off()


    def handle_button_press(self):

        self.blink(3,self.TIME_INTERVAL)

        now = datetime.now()
        
        

        ret, image = self.cam.read()
        if not ret:
            print("failed to grab frame")
            return
        
        image = image.reshape((self.HEIGHT, self.WIDTH, 3))
        print("snapped")
       

        ids, new_faces = get_image_face_ids(image, self.known_faces)
        save_new_faces(new_faces, self.ENCODING_DIR)

        print("Found: {}".format(ids))

        

        fileName = 'data/captures/{}.jpg'.format(
            now.strftime("%m-%d-%yT%H-%M-%S"))
        cv2.imwrite(fileName, image)
        

    def run(self):
        self.button.when_activated = self.handle_button_press

        while True:
            self.button.wait_for_press()

          


snapper = Snapper()
snapper.run()
