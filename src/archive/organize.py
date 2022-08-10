import glob
import os
import face_recognition
import numpy as np

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

        