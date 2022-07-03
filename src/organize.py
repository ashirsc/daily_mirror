import face_recognition
import cv2
import numpy as np
import os
import glob

faces_encodings = []
faces_names = []

cur_direc = os.getcwd()
train_dir = 'data/faces/'
people_dir = 'data/people/'
capture_dir = 'data/captures/'


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
    faces_encodings.append(imageData['image_encoding_{}'.format(i)])

    # Create array of known names
    names[i] = names[i].replace(cur_direc, "")
    names[i] = names[i].replace(train_dir, "")
    names[i] = names[i].replace("\\", "")
    names[i] = os.path.splitext(names[i])[0]
    faces_names.append(names[i])




capture_path = os.path.join(cur_direc, capture_dir)
print("reading files at {}".format(capture_path))
list_of_files = [f for f in glob.glob(capture_path+'*.jpg')]
print("Found {} files".format(len(list_of_files)))
number_files = len(list_of_files)


for i in range(number_files):
    currentImage = face_recognition.load_image_file(list_of_files[i])
    face_locations = face_recognition.face_locations( currentImage)
    face_encodings = face_recognition.face_encodings( currentImage, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(faces_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance( faces_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = faces_names[best_match_index]

        face_names.append(name)

    for j in range(len(face_names)):
        file_name = list_of_files[i].replace(capture_dir, os.path.join(people_dir + face_names[j]+ "/" ))
        currentImage = cv2.cvtColor(currentImage, cv2.COLOR_BGR2RGB)
        cv2.imwrite(file_name,currentImage)

    os.remove(list_of_files[i])
