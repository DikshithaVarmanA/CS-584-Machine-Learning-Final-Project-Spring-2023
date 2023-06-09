# -*- coding: utf-8 -*-
"""Untitled9.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_YEGxNmOO5HvP3vgEWdj1Zg5v09_-ao1
"""

import numpy as np
import tensorflow as tf

with open("/content/fer2013.csv") as f: content = f.readlines()

lines = np.array(content)
num_of_instances = lines.size 
print("number of instances: ",num_of_instances) 
print("instance length: ",len(lines[1].split(",")[1].split(" ")))

num_classes = 7 #angry, disgust, fear, happy, sad, surprise, neutral

x_train, y_train, x_test, y_test = [], [], [], []

for i in range(1,num_of_instances): 
  emotion, img, usage = lines[i].split(",") 
  val = img.split(" ") 
  pixels = np.array(val, 'float32') 
  emotion = tf.keras.utils.to_categorical(emotion, num_classes) 
  if 'Training' in usage: 
    y_train.append(emotion) 
    x_train.append(pixels) 
  elif 'PublicTest' in usage: 
    y_test.append(emotion) 
    x_test.append(pixels)

x_train = np.array(x_train, 'float32') 
y_train = np.array(y_train, 'float32') 
x_test = np.array(x_test, 'float32') 
y_test = np.array(y_test, 'float32')

import numpy as np

# Convert lists to numpy arrays
x_train = np.array(x_train)
x_test = np.array(x_test)

# Normalize inputs between [0, 1]
x_train /= 255
x_test /= 255

# Reshape and convert to float32
x_train = x_train.reshape(x_train.shape[0], 48, 48, 1).astype('float32')
x_test = x_test.reshape(x_test.shape[0], 48, 48, 1).astype('float32')

print(x_train.shape) 
print(y_train.shape) 
print(x_test.shape) 
print(y_test.shape)

# Build the model
emo_model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(64, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(128, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(256, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(256, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(256, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Conv2D(512, kernel_size=3, activation='relu', padding='same', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.MaxPool2D(pool_size=2, strides=2, padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Flatten(), 
    tf.keras.layers.Dense(units = 4096, activation ='relu', kernel_initializer='he_normal'), 
    tf.keras.layers.Dropout(0.5), 
    tf.keras.layers.Dense(units = 4096, activation ='relu', kernel_initializer='he_normal'), 
    tf.keras.layers.Dropout(0.5), 
    tf.keras.layers.Dense(units = 1000, activation ='relu', kernel_initializer='he_normal'), 
    tf.keras.layers.Dense(units = 7, activation ='softmax') 
    ])

predictions = emo_model(x_train[1:2]).numpy() 
print(predictions)

sgd = tf.keras.optimizers.SGD( learning_rate=0.0001, momentum=0.85, nesterov=True )
loss_fn = tf.keras.losses.CategoricalCrossentropy(from_logits=True)

emo_model.compile(optimizer=sgd, loss=loss_fn, metrics=['accuracy'])

batch_size = 113 # try several values 
train_DataGen = tf.keras.preprocessing.image.ImageDataGenerator(zoom_range=0.2, width_shift_range=0.1, height_shift_range = 0.1, horizontal_flip=True) 
train_set_conv = train_DataGen.flow(x_train, y_train, batch_size=batch_size) # train_lab is categorical

history = emo_model.fit(train_set_conv, epochs=400, steps_per_epoch=x_train.shape[0]//batch_size, validation_data=(x_test, y_test), verbose=1)

train_score = emo_model.evaluate(x_train, y_train, verbose=0) 
print('Train loss:', train_score[0]) 
print('Train accuracy:', 100*train_score[1]) 
test_score = emo_model.evaluate(x_test, y_test, verbose=0) 
print('Test loss:', test_score[0]) 
print('Test accuracy:', 100*test_score[1])

