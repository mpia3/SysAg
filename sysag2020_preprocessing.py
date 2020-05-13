# -*- coding: utf-8 -*-
"""SysAg2020 Preprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z1mQ9wUuH9IA7N1JZl5yjYkG1H9C6HrW
"""

# !pip install git+https://github.com/rcmalli/keras-vggface.git
# # https://github.com/rcmalli/keras-vggface
# !pip show keras-vggface
# !pip install mtcnn
# !pip install face_recognition

# Commented out IPython magic to ensure Python compatibility.
# from google.colab import drive
# from google.colab.patches import cv2_imshow
# drive.mount('/gdrive')
# %cd /gdrive

import keras_vggface
import mtcnn
import face_recognition
import os
from matplotlib import pyplot
from PIL import Image
from numpy import asarray
from mtcnn.mtcnn import MTCNN
import cv2
"""
Script di pre processing
Utile per:
-   Estrarre i volti da immagini complete 
-   Estrarre la linea degli occhi (solo volti senza maschera)
"""

ActorsPath = '/gdrive/My Drive/SysAgTest'
ActorsCroppedPath = '/gdrive/My Drive/SysAgDatasetFaceOnly/Test'

# from google.colab.patches import cv2_imshow


# extract a single face from a given photograph
def extract_face(filename, required_size=(224, 224)):
    """
    Estrattore del volto a dimensione 224x224
    :param filename: immagine input
    :param required_size:  dimensione target
    :return: matrice di pixel (immagine)
    """
    # load image from file
    pixels = pyplot.imread(filename)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]['box']
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize(required_size)
    face_array = asarray(image)
    return face_array


def cropEyeLine(pixels, x, y):
    """
    Taglia linea degli occhi
    :param pixels:
    :param x:
    :param y:
    :return: cropped image
    """
    crop = pixels[0:y][0:x]
    # cv2_imshow(crop)
    return crop


def printImage(image):
    """
    Stampa a video immagine (matrice di pixel)
    :param image:
    :return:
    """
    pyplot.imshow(image)
    pyplot.show()


def cropFaceOnly(ActorsPath, ActorsCroppedPath):
    """
    Taglia il volto dall'immagine intera
    :param ActorsPath: path di input
    :param ActorsCroppedPath: path di output
    :return: None
    """
    listOfActors = os.listdir(ActorsPath)
    print("Actors: ", listOfActors)

    for actor in listOfActors:
        actorImages = os.listdir(ActorsPath + '/' + actor)
        print(actor, " = ", actorImages)
        for actorImage in actorImages:
            print("-----------------------------------------------------------------")
            # load the photo and extract the face
            fullpath = ActorsPath + '/' + actor + '/' + actorImage
            outputpath = ActorsCroppedPath + '/' + actor + '/' + actorImage

            try:
                img = extract_face(fullpath)
                printImage(img)
                print(fullpath)
                print(outputpath)
                pyplot.imsave(outputpath, img)
            except:
                print("Failed: ", actorImage)


def cropEyeLineByFace(ActorsPath, ActorsCroppedPath):
    """
    Taglio del volto basato sui punti facciali
    :param ActorsPath: path di input
    :param ActorsCroppedPath: path di output
    :return: None
    """
    listOfActors = os.listdir(ActorsPath)
    print("Actors: ", listOfActors)

    for actor in listOfActors:
        actorImages = os.listdir(ActorsPath + '/' + actor)
        print(actor, " = ", actorImages)
        for actorImage in actorImages:
            print("-----------------------------------------------------------------")
            # load the photo and extract the face
            fullpath = ActorsPath + '/' + actor + '/' + actorImage
            outputpath = ActorsCroppedPath + '/' + actor + '/' + actorImage

            try:
                img = extract_face(fullpath)
                img = face_recognition.load_image_file(fullpath)

                faceCoords2 = face_recognition.face_locations(img)
                landMarks = face_recognition.face_landmarks(img, faceCoords2)
                top = faceCoords2[0][0]
                right = faceCoords2[0][1]
                down = faceCoords2[0][2]
                left = faceCoords2[0][3]

                topleft = (faceCoords2[0][3], faceCoords2[0][0])
                bottomright = (faceCoords2[0][1], faceCoords2[0][2])

                print('right_eye = ', landMarks[0]['right_eye'])
                print('left_eye = ', landMarks[0]['left_eye'])
                print('nose_bridge = ', landMarks[0]['nose_bridge'])

                landMarksGood = list()
                landMarksGood.append(landMarks[0]['right_eye'])
                landMarksGood.append(landMarks[0]['left_eye'])
                landMarksGood.append(landMarks[0]['nose_bridge'])

                listMinY = list()
                for landMark in landMarksGood:
                    for coord in landMark:
                        listMinY.append(coord[1])
                TotalMin = min(listMinY)
                # print("Total min: ",min(listMinY))

                # printImage(img)

                offset = 30
                pixelsCropped = cropEyeLine(img, right, TotalMin + offset)

                printImage(img)
                print(fullpath)
                print(outputpath)
                # pyplot.imsave(outputpath, img)
                cv2.imwrite(outputpath, img)

            except:
                print("Failed: ", actorImage)