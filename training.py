import tensorflow as tf
import os
import cv2
import imghdr
import keras
import numpy as np
from matplotlib import pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.models import load_model


gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

tf.config.list_physical_devices('GPU')

def main():
    #read in the data
    data = tf.keras.utils.image_dataset_from_directory('test_data', batch_size=32).map(lambda x,y: (x/255, y))

    #split the data into training set and test set
    train_size = int(len(data)*.6)
    val_size = int(len(data)*.2)
    test_size = int(len(data)*.2)

    train = data.take(train_size)
    val = data.skip(train_size).take(val_size)
    test = data.skip(train_size+val_size).take(test_size)

    #create the model and define the layers
    model = Sequential()

    model.add(keras.Input(shape=(256, 256, 3)))
    model.add(Conv2D(16, (3,3), 1, activation='relu'))
    model.add(MaxPooling2D())
    model.add(Conv2D(32, (3,3), 1, activation='relu'))
    model.add(MaxPooling2D())
    model.add(Conv2D(16, (3,3), 1, activation='relu'))
    model.add(MaxPooling2D())
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile('adam', loss=tf.losses.BinaryCrossentropy(), metrics=['accuracy'])


    #get overview and summary of model
    model.summary()

    #train the model weights
    model.fit(train, epochs=50, validation_data=val)

    model.save('pineapple_CNN.keras')


if __name__ == "__main__":
    main()

