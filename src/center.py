import cv2
import numpy as np
import os
import glob
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


def drawCross(img):
    height, width, z = img.shape
    mx = int(round(width/2))
    my = int(round(height/2))
    cv2.line(img=img, pt1=(0, my), pt2=(
        width, my), color=(0, 0, 255), thickness=3)
    cv2.line(img=img, pt1=(mx, 0), pt2=(
        mx, height), color=(0, 0, 255), thickness=3)

    return img


def getPixelCoors(img, x, y):
    height, width, z = img.shape
    pixelX = int(round(x * width))
    pixelY = int(round(y * height))

    return (pixelX, pixelY)


def normPic(img, x, y):

    height, width, z = img.shape
    xstart = 0
    ystart = 0
    xend = width
    yend = height

    if(x < .5):
        # shave of right side
        pixelDiff = (.5 - x) * width * 2
        xend = int(round(width - pixelDiff))
    else:
        pixelDiff = (x - .5) * width * 2
        xstart = int(round(pixelDiff))
    if(y < .5):
        # shave of bottom
        pixelDiff = (.5 - y) * height * 2
        yend = int(round(height - pixelDiff))
    else:
        # shave of top
        pixelDiff = (y-.5) * height * 2
        ystart = int(round(pixelDiff))

    return img[ystart:yend, xstart:xend]


cur_direc = os.getcwd()
people_dir = 'data/people/'


path = os.path.normpath(os.path.join(cur_direc, people_dir, "drew"))


IMAGE_FILES = [f for f in glob.glob(path+'/*.jpg')]


with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    for idx, file in enumerate(IMAGE_FILES):
        image = cv2.imread(file)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(
            cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        # Draw face detections of each face.
        if not results.detections:
            continue
        annotated_image = image.copy()
        midpointX = 0
        midpointY = 0
        for detection in results.detections:
            left_eye = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.LEFT_EYE)
            right_eye = mp_face_detection.get_key_point(
                detection, mp_face_detection.FaceKeyPoint.RIGHT_EYE)
            midpointX = ((left_eye.x + right_eye.x) / 2)
            midpointY = ((left_eye.y + right_eye.y) / 2)

            # mp_drawing.draw_detection(annotated_image, detection)
            # cv2.circle(img=annotated_image, center=(getPixelCoors(annotated_image, midpointX, midpointY)),
            #            radius=5, color=(0, 0, 255), thickness=3)

        normedImg = normPic(annotated_image, midpointX, midpointY)
        cv2.imwrite(os.path.join(path, 'processed/annotated_image' +
                    str(idx) + '.jpg'), normedImg)
