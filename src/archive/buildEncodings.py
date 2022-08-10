import face_recognition
# import cv2
import numpy as np
import os
import glob

faces_encodings = []
faces_names = []

cur_direc = os.getcwd()
train_dir = 'data/faces/'

path = os.path.join(cur_direc, train_dir)
print("Reading files at {}".format(path))

list_of_files = [f for f in glob.glob(path+'*.jpg')]
print("Found {} files".format(len(list_of_files)))
number_files = len(list_of_files)


imageData = {}

for i in range(number_files):
    imageData['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
    imageData['image_encoding_{}'.format(i)] = face_recognition.face_encodings(imageData['image_{}'.format(i)])[0]
    faces_encodings.append(imageData['image_encoding_{}'.format(i)])
    faces_names.append(os.path.basename(list_of_files[i]).split('.')[0])
    np.save('data/encodings/{}.npy'.format(faces_names[i]), faces_encodings[i])

print(faces_names)


