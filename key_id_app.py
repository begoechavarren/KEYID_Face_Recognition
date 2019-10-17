import keras
from keras import backend as K
import cv2
import os
import src.functions_app as functions_app
import src.tkinter_display as tkinter_display

# disable Tensorflow warning
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# connect to mySQL database
mydb = functions_app.mySQLdb_connect()
mycursor = mydb.cursor()

# load face cascade
face_cascade = cv2.CascadeClassifier(
    './files/haarcascade_frontalface_default.xml')

# load the saved images dict
names = functions_app.load_names('./files/images.pickle')

# load the saved model
model = keras.models.load_model('./files/model.h5')

# display the tkinter GUI
tkinter_display.tkinter_display(model, face_cascade, names, mydb, mycursor)
