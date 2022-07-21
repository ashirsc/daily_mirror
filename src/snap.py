import glob
import os
import face_recognition
import sys
import signal
from gpiozero import Button, LED
from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from datetime import datetime
import cv2
import numpy as np
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection


class Organizer:
    def __init__(self) -> None:
        print("Initializing organizer.")
        self.faces_encodings = []
        self.faces_names = []

        cur_direc = os.getcwd()
        train_dir = 'data/faces/'

        path = os.path.join(cur_direc, train_dir)
        print("reading files at {}".format(path))
        list_of_files = [f for f in glob.glob(path+'*.jpg')]
        print("Found {} files".format(len(list_of_files)))
        number_files = len(list_of_files)
        names = list_of_files.copy()

        imageData = {}

        for i in range(number_files):
            imageData['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])


            imageData['image_encoding_{}'.format(i)] = face_recognition.face_encodings(imageData['image_{}'.format(i)])[0]
            self.faces_encodings.append(imageData['image_encoding_{}'.format(i)])

            # Create array of known names
            names[i] = names[i].replace(cur_direc, "")
            names[i] = names[i].replace(train_dir, "")
            names[i] = names[i].replace("/", "")
            names[i] = os.path.splitext(names[i])[0]
            self.faces_names.append(names[i])
            print("Organizer initialized.")

    def matchFace(self, currentImage):
        face_locations = face_recognition.face_locations( currentImage)
        face_encodings = face_recognition.face_encodings( currentImage, face_locations)

        # face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.faces_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance( self.faces_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.faces_names[best_match_index]

            # face_names.append(name)
            return name

        


class Snapper:
    pause = False

    TIME_INTERVAL = .5

    VERT_UPPER_LIMIT = 0.3
    VERT_LOWER_LIMIT = 0.6
    HORZ_RIGHT_LIMIT = 0.6
    HORZ_LEFT_LIMIT = 0.4

    HEIGHT, WIDTH = 240, 320

    def __init__(self):
        self.organizer = Organizer()
        self.camera = PiCamera()
        self.camera.resolution = (self.WIDTH, self.HEIGHT)
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

    def drawValidZone(self, img):

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

    def drawMidpoint(self, img, midpoint):
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
        

        image = np.empty((self.HEIGHT * self.WIDTH * 3), dtype=np.uint8)

        self.camera.capture(image, 'bgr')
        image = image.reshape((self.HEIGHT, self.WIDTH, 3))
        print("snapped")

        name = self.organizer.matchFace(image)
        print("Found: {}".format(name))

        # is there a dir for the name in the capture dir
        

        fileName = 'data/captures/{}/{}.jpg'.format(
            name,
            now.strftime("%m-%d-%yT%H-%M-%S"))
        cv2.imwrite(fileName, image)
        
        self.pause = False

    def run(self):

        while True:
            if not self.pause:
                image = np.empty(
                    (self.HEIGHT * self.WIDTH * 3), dtype=np.uint8)
                self.camera.capture(image, 'bgr')
                image = image.reshape((self.HEIGHT, self.WIDTH, 3))

                # cv2.imwrite("feed.jpg", image)

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
