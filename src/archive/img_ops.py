import cv2

import mediapipe as mp
mp_face_detection = mp.solutions.face_detection

  VERT_UPPER_LIMIT = 0.3
    VERT_LOWER_LIMIT = 0.6
    HORZ_RIGHT_LIMIT = 0.6
    HORZ_LEFT_LIMIT = 0.4


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
