import matplotlib.pyplot as plt
import numpy as np
import PIL
import pandas as pd
import random

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import os

from tensorflow import keras

def process_data(dataset_path):
    data = tf.keras.utils.image_dataset_from_directory(dataset_path)
    data = data.map(lambda x,y:(x/255,y))
    return data

train_data_dir = 'Data/Currency Type/Train_currency'
val_data_dir='Data/Currency Type/Val_currency'
test_data_dir='Data/Currency Type/Test_currency'

train_data = process_data(train_data_dir)
val_data = process_data(val_data_dir)
test_data = process_data(test_data_dir)




model = Sequential([
  layers.Conv2D(16, (3,3), 1, activation='relu',input_shape = (256,256,3)),
  layers.MaxPooling2D(),

  layers.Conv2D(32, (3,3), 1, activation='relu'),
  layers.MaxPooling2D(),

  layers.Conv2D(16, (3,3), 1, activation='relu'),
  layers.MaxPooling2D(),

  layers.Flatten(),

  layers.Dense(256, activation='relu'),
  layers.Dense(4,activation='softmax')
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])
logdir = 'logs'
tensorboard_callbacks = tf.keras.callbacks.TensorBoard(log_dir=logdir)
filepath = 'ModelCheckpoints/checkpoint-CURRENCY-{epoch:02d}-{val_loss:.02f}.hdf5'
checkpoint = tf.keras.callbacks.ModelCheckpoint(filepath,monitor='val_loss',verbose=1,save_best_only=True,mode='min', save_weights_only=False)
model.fit(train_data,epochs=5,validation_data=val_data,callbacks=[tensorboard_callbacks,checkpoint])
test_loss,test_acc = model.evaluate(test_data)
print('Test Accuracy {} Test loss {}'.format(test_acc,test_loss))


model_path = os.path.join('Models','CURRENCYpoeAI.h5')


