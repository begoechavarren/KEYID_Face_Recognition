from __future__ import print_function
import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import src.functions_img_processing as functions_img_processing
import os


def train_model(face_cascade, model_path='./files/model.h5'):
    # disable Tensorflow warning
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # process images
    # video_to_images() --> if input was in video format
    images = functions_img_processing.images_to_dict(face_cascade)
    functions_img_processing.save_images(images)

    # generate model variables
    num_classes = len(images)
    X, y = functions_img_processing.X_y_generator(images)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)

    # prepare data to feed the NN
    num_classes = num_classes
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    print("X.shape --> {}".format(X.shape))
    print("y.shape --> {}".format(y.shape))

    # neural network architecture: VGG-like convnet
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation='relu',
                     input_shape=X.shape[1:]))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

    # Fit the NN
    batch_size = 10
    epochs = 10

    model.fit(X_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              verbose=1,
              validation_data=(X_test, y_test))

    if os.path.exists(model_path):
        os.remove(model_path)

    model.save(model_path)
