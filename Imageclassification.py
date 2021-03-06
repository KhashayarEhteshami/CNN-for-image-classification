# -*- coding: utf-8 -*-
import os
from numpy import mean
from numpy import std
from matplotlib import pyplot
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense, Conv2D, MaxPooling2D
import pandas as pd
from keras_preprocessing.image import ImageDataGenerator
import numpy as np
import tensorflow as tf
from tensorflow.python.keras.layers.preprocessing import image_preprocessing
from tensorflow.python.keras.preprocessing import dataset_utils
from tensorflow.python.keras.preprocessing import image as keras_image_ops
from tensorflow.python.ops import image_ops
from tensorflow.python.ops import io_ops
from tensorflow.python.util.tf_export import keras_export
import matplotlib.pyplot as plt
import PIL
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
import pathlib
from keras.models import load_model

batch_size = 32
img_height = 32
img_width = 32

train_dataset = tf.keras.preprocessing.image_dataset_from_directory(dir,
  validation_split=0.2,
  subset="training", label_mode='categorical', shuffle=True,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

validation_dataset = tf.keras.preprocessing.image_dataset_from_directory(
  dir,
  validation_split=0.2,
  subset="validation",  label_mode='categorical', shuffle=True,
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

class_names = train_dataset.class_names
print(class_names)

normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)

val_batches = tf.data.experimental.cardinality(validation_dataset)
test_dataset = validation_dataset.take(val_batches // 5)
validation_dataset = validation_dataset.skip(val_batches // 5)

# define model
num_classes = 26

model = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, 3, activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(optimizer='Adam', 
              loss='categorical_crossentropy', 
              metrics =['accuracy'])

epoch = 70
history = model.fit(train_dataset, epochs=epoch, steps_per_epoch=50, verbose=1, validation_data=validation_dataset, validation_steps=10)
model.save_weights("weights.h5")
model.save("/Myfinalmodel")

# evaluate model
los = model.evaluate(validation_dataset, steps=70)

model.summary()

acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc))

fig = plt.figure(figsize=(14,7))
plt.plot(epochs, acc, 'r', label="Training Accuracy")
plt.plot(epochs, val_acc, 'b', label="Validation Accuracy")
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Training and validation accuracy')
plt.legend(loc='lower right')
plt.show()

fig2 = plt.figure(figsize=(14,7))
plt.plot(epochs, loss, 'r', label="Training Loss")
plt.plot(epochs, val_loss, 'b', label="Validation Loss")
plt.legend(loc='upper right')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and validation loss')

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(70)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

predictions = model.predict(test_dataset, batch_size=64, verbose=1)
answer = np.argmax(predictions, axis=1)
print(answer)

predictions = np.array([])
labels =  np.array([])
for x, y in test_dataset:
    predictions = np.concatenate([predictions, np.argmax(model.predict(x), axis = -1)])
    labels = np.concatenate([labels, np.argmax(y.numpy(), axis=-1)])
confusionMatrix = tf.math.confusion_matrix(labels=labels, predictions=predictions).numpy()

confusionMatrix

def accuracy(confusionMatrix):
    diagonal_sum = confusionMatrix.trace()
    sum_of_all_elements = confusionMatrix.sum()
    return diagonal_sum / sum_of_all_elements

accuracy(confusionMatrix)
