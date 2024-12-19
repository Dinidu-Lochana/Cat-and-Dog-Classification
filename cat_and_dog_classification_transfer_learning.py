# -*- coding: utf-8 -*-
"""Cat-and-Dog-Classification-Transfer-Learning.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FhxvdpzufO1rU7wVjLR6ifmi7uhrSZJ9
"""

!pip install numpy -q
!pip install pandas -q
!pip install matplotlib -q
!pip install tensorflow -q

!pip install opendatasets -q

"""# **Importing Libraries**"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import opendatasets as od

od.download("https://www.kaggle.com/datasets/tongpython/cat-and-dog")

Batch_size = 32
Image_size = (128,128)

train_data_dir = "/content/cat-and-dog/training_set/training_set"
test_data_dir = "/content/cat-and-dog/test_set/test_set"

train_data = tf.keras.utils.image_dataset_from_directory(train_data_dir,
                                                       image_size = Image_size,
                                                       batch_size = Batch_size,
                                                       subset = 'training',
                                                       validation_split = 0.1,
                                                       seed = 42)

validation_data = tf.keras.utils.image_dataset_from_directory(train_data_dir,
                                                       image_size = Image_size,
                                                       batch_size = Batch_size,
                                                       subset = 'validation',
                                                       validation_split = 0.1,
                                                       seed = 42)

test_data = tf.keras.utils.image_dataset_from_directory(test_data_dir,
                                                       image_size = Image_size,
                                                       batch_size = Batch_size)

"""# **Dataset Description**"""

class_names = train_data.class_names
class_names

for image_batch,label_batch in train_data.take(1):
  print(image_batch.shape)
  print(label_batch.shape)

plt.figure(figsize=(10,4))
for image,label in train_data.take(1):
  for i in range(12):
    ax = plt.subplot(2,6,i+1)
    plt.imshow(image[i].numpy().astype("uint8"))
    plt.title(class_names[label[i]])
    plt.axis("off")

"""# **Data Preprocessing**"""

for image,label in train_data.take(1):
  for i in range(1):
    print(image)

train_data = train_data.map(lambda x,y : (x/255,y))
validation_data = validation_data.map(lambda x,y : (x/255,y))
test_data = test_data.map(lambda x,y : (x/255,y))

for image,label in train_data.take(1):
  for i in range(1):
    print(image)

"""# **Transfer Leaning**"""

pretrained_model = tf.keras.applications.Xception(
    include_top=False,
    weights='imagenet',
    input_tensor=None,
    input_shape=(128,128,3),
    pooling='max'
)

for layer in pretrained_model.layers:
  layer.trainable = False

"""# **Model Implementation**"""

# Data Augmentation
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical", input_shape=(128, 128, 3)),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomContrast(0.2),
    tf.keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1),
])

model = tf.keras.Sequential()

model.add(pretrained_model)


# Flatten and dense layers
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(512, activation='relu'))

model.add(tf.keras.layers.BatchNormalization())
model.add(tf.keras.layers.Dropout(0.3))

model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

model.summary()

model.compile(optimizer=tf.keras.optimizers.Adam(),
              loss=tf.keras.losses.BinaryCrossentropy(),
              metrics=['accuracy'])

history = model.fit(train_data,
                    epochs=10,
                    validation_data=validation_data)

fig = plt.figure()
plt.plot(history.history['loss'], color='teal', label='loss')
plt.plot(history.history['val_loss'], color='orange', label='val_loss')
fig.suptitle('Loss', fontsize=20)
plt.legend()
plt.show()

fig = plt.figure()
plt.plot(history.history['accuracy'], color='teal', label='accuracy')
plt.plot(history.history['val_accuracy'], color='orange', label='val_accuracy')
fig.suptitle('Accuracy', fontsize=20)
plt.legend()
plt.show()

"""# **Model Evaluation**"""

precision = tf.keras.metrics.Precision()
recall = tf.keras.metrics.Recall()
accuracy = tf.keras.metrics.BinaryAccuracy()

for batch in test_data.as_numpy_iterator():
    X, y = batch
    yhat = model.predict(X)
    precision.update_state(y, yhat)
    recall.update_state(y, yhat)
    accuracy.update_state(y, yhat)

precision.result().numpy(), recall.result().numpy(), accuracy.result().numpy()

!pip install opencv-python

import cv2

image = cv2.imread('/content/cat-and-dog/test_set/test_set/cats/cat.4330.jpg')
plt.imshow(image)
plt.show()

resized_image = tf.image.resize(image, Image_size)
scaled_image = resized_image/255

scaled_image

np.expand_dims(scaled_image,0).shape

y_hat = model.predict(np.expand_dims(scaled_image,0))

y_hat

class_names

if y_hat > 0.5:
    print(f'Predicted class is Dog')
else:
    print(f'Predicted class is Cat')