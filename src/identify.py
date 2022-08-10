from email.mime import image
from uuid import uuid4
import face_recognition as fr
import cv2
import numpy as np
import os
import glob

from dataclasses import dataclass


@dataclass
class eFace:
    id: str
    encoding: np.ndarray

# pass the path to a dir with *.npy encodings files
def load_encodings(encodings_dir) -> list:

    # Load in references
    encoding_ref_files = [f for f in glob.glob(encodings_dir+'*.npy')]

    eFaces = []
    print('Loading encodings...')

    for i in range(len(encoding_ref_files)):
        eFaces.append(eFace(os.path.basename(encoding_ref_files[i]).split(
            '.')[0], np.load(encoding_ref_files[i])))

    print("loaded: {}".format(list(map(lambda x: x.id, eFaces))))
    return eFaces

def get_img_encodings(img):
    face_locations = fr.face_locations(img)
    return fr.face_encodings(img, face_locations)

def get_image_face_ids(img, ref_faces):

    img_encodings = get_img_encodings(img)


    ids = []
    new_faces = []
    ref_encodings = list(map(lambda x: x.encoding, ref_faces))

    for encoding in img_encodings:
        name = "Unknown"

        matches = fr.compare_faces(ref_encodings, encoding)
        face_distances = fr.face_distance( ref_encodings, encoding)


        if face_distances.size > 0:

            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = ref_faces[best_match_index].id
            else:
                name = str(uuid4())[0:8]
                face = eFace(name, encoding)
                new_faces.append(face)
        else:
            name = str(uuid4())[0:8]
            face = eFace(name, encoding)
            new_faces.append(face)

        ids.append(name)
    return ids, new_faces

def save_new_faces(new_faces, encodings_dir):
    for face in new_faces:
        np.save(os.path.join(encodings_dir, face.id+'.npy'), face.encoding)
        print("Saved {}'s encoding".format(face.id))


cur_direc = os.getcwd()
capture_dir = 'data/people/drew/'
encodings_dir = 'data/encodings/'

# path = os.path.join(cur_direc, capture_dir)
# print("Reading files at {}".format(path))
# image_files = [f for f in glob.glob(path+'*.jpg')]
# print("Found {} files".format(len(image_files)))

encoding_refs = load_encodings(encodings_dir)
img = fr.load_image_file("data/people/drew/07-03-22T08-07-13.jpg")

ids, new_faces = get_image_face_ids(img, encoding_refs)
save_new_faces(new_faces, encodings_dir)

print("found {}".format(ids))




