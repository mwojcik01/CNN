# -*- coding: utf-8 -*-
"""bezAUG_DOBRE_Sieć_CNN_2_klasy_90.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xzYJQwRIpVTb1rRTzqQt5_xgjvZfLEle
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import shutil
import plotly.graph_objects as go
from sklearn.metrics import confusion_matrix, classification_report
 
 
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array
from tensorflow.keras.models import Sequential
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import TensorBoard
 
np.set_printoptions(precision=6, suppress=True)

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
from keras import backend as K
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

#from google.colab import drive
#drive.mount('/content/drive')

!unzip -uq "/content/drive/My Drive/base_ddsm_cbm_2.zip" -d "./" # wypakowanie plików z Drive

base_dir = './base_ddsm_cbm_2' # obliczanie ilości plików w każdym folderze
raw_no_of_files = {}
classes = ['ben_mal', 'nor']
for dir in classes:
    raw_no_of_files[dir] = len(os.listdir(os.path.join(base_dir, dir)))

raw_no_of_files.items()

import os
import shutil
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

data_dir = './images' # tworzenie katalogów: treningowego, walidacyjnego oraz testowego. 
                      #w każdym znajdują się 2 foldery: nor, ben_mal

if not os.path.exists(data_dir):
    os.mkdir(data_dir)

train_dir = os.path.join(data_dir, 'train')
valid_dir = os.path.join(data_dir, 'valid')
test_dir = os.path.join(data_dir, 'test')

train_nor_dir = os.path.join(train_dir, 'nor')
train_ben_mal_dir = os.path.join(train_dir, 'ben_mal')

valid_nor_dir = os.path.join(valid_dir, 'nor')
valid_ben_mal_dir = os.path.join(valid_dir, 'ben_mal')

test_nor_dir = os.path.join(test_dir, 'nor')
test_ben_mal_dir = os.path.join(test_dir, 'ben_mal')

for directory in (train_dir, valid_dir, test_dir):
    if not os.path.exists(directory):
        os.mkdir(directory)

dirs = [train_nor_dir, train_ben_mal_dir, valid_nor_dir, valid_ben_mal_dir, test_nor_dir, test_ben_mal_dir]

for dir in dirs:
    if not os.path.exists(dir):
        os.mkdir(dir)

#kopiowanie
nor_fnames = os.listdir(os.path.join(base_dir, 'nor'))
ben_mal_fnames = os.listdir(os.path.join(base_dir, 'ben_mal'))


nor_fnames = [fname for fname in nor_fnames if fname.split('.')[1].lower() in ['png']]
ben_mal_fnames = [fname for fname in ben_mal_fnames if fname.split('.')[1].lower() in ['png']]

size = min(len(nor_fnames), len(ben_mal_fnames)) # ustalanie ilości plików w folderze 

train_size = int(np.floor(0.7 * size))
valid_size = int(np.floor(0.2 * size))
test_size = size - train_size - valid_size

train_idx = train_size
valid_idx = train_size + valid_size
test_idx = train_size + valid_size + test_size

for i, fname in enumerate(nor_fnames): # proces kopiowania plików
    if i <= train_idx:
        src = os.path.join(base_dir, 'nor', fname)
        dst = os.path.join(train_nor_dir, fname)
        shutil.copyfile(src, dst)
    elif train_idx < i <= valid_idx:
        src = os.path.join(base_dir, 'nor', fname)
        dst = os.path.join(valid_nor_dir, fname)
        shutil.copyfile(src, dst) 
    elif valid_idx < i < test_idx:
        src = os.path.join(base_dir, 'nor', fname)
        dst = os.path.join(test_nor_dir, fname)
        shutil.copyfile(src, dst) 

for i, fname in enumerate(ben_mal_fnames):
    if i <= train_idx:
        src = os.path.join(base_dir, 'ben_mal', fname)
        dst = os.path.join(train_ben_mal_dir, fname)
        shutil.copyfile(src, dst)
    elif train_idx < i <= valid_idx:
        src = os.path.join(base_dir, 'ben_mal', fname)
        dst = os.path.join(valid_ben_mal_dir, fname)
        shutil.copyfile(src, dst) 
    elif valid_idx < i < test_idx:
        src = os.path.join(base_dir, 'ben_mal', fname)
        dst = os.path.join(test_ben_mal_dir, fname)
        shutil.copyfile(src, dst)

# sprawdzanie ilości plików w folderach
print('nor - trening', len(os.listdir(train_nor_dir))) 
print('nor - walidacja', len(os.listdir(valid_nor_dir)))
print('nor - test', len(os.listdir(test_nor_dir)))

print('ben_mal - trening', len(os.listdir(train_ben_mal_dir)))
print('ben_mal - walidacja', len(os.listdir(valid_ben_mal_dir)))
print('ben_mal - test', len(os.listdir(test_ben_mal_dir)))

from keras.preprocessing.image import ImageDataGenerator

# przeskalowanie obrazów o współczynnik 1/255
train_datagen = ImageDataGenerator(rescale=1./255.)
valid_datagen = ImageDataGenerator(rescale=1./255.)

train_generator = train_datagen.flow_from_directory(directory=train_dir,
                                                   target_size=(128, 128),
                                                   batch_size=20,
                                                   class_mode='binary')

valid_generator = valid_datagen.flow_from_directory(directory=valid_dir,
                                                   target_size=(128, 128),
                                                   batch_size=20,
                                                   class_mode='binary')

model = Sequential(
    [
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu", input_shape=(128, 128, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation='relu'),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
#        layers.Dropout(0.5),
        layers.Dense(units=256, activation='relu'),
        layers.Dense(units=1, activation='sigmoid') #1 sigmoid, 3 softmax
    ]
)

model.summary()

model.compile(optimizer='Adam',
             loss='binary_crossentropy',
             metrics=['accuracy'])

batch_size = 16
steps_per_epoch = train_size // batch_size
validation_steps = valid_size // batch_size

#batch_size = 32
#steps_per_epoch = train_size_ben_mal // batch_size
#validation_steps = valid_size_ben_mal // batch_size

history = model.fit(train_generator,
                    steps_per_epoch=100, #steps_per_epoch
                    epochs=40,    # 100
                    validation_data=valid_generator,
                    validation_steps=validation_steps
                    )

def plot_hist(history):
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist['epoch'], y=hist['accuracy'], name='accuracy', mode='markers+lines'))
    fig.add_trace(go.Scatter(x=hist['epoch'], y=hist['val_accuracy'], name='val_accuracy', mode='markers+lines'))
    fig.update_layout(width=1000, height=500, title='Accuracy vs. Val Accuracy', xaxis_title='Epoki', yaxis_title='Accuracy', yaxis_type='log')
    fig.show()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist['epoch'], y=hist['loss'], name='loss', mode='markers+lines'))
    fig.add_trace(go.Scatter(x=hist['epoch'], y=hist['val_loss'], name='val_loss', mode='markers+lines'))
    fig.update_layout(width=1000, height=500, title='Loss vs. Val Loss', xaxis_title='Epoki', yaxis_title='Loss', yaxis_type='log')
    fig.show()

plot_hist(history)

test_datagen = ImageDataGenerator(rescale=1./255.)
test_generator = test_datagen.flow_from_directory(test_dir,
                                                 target_size=(128, 128),
                                                 batch_size=8,
                                                 class_mode='binary')

test_loss, test_acc = model.evaluate(test_generator, steps=50)
print('Dokładność testowania:', test_acc)

from tensorflow.keras.preprocessing.image import ImageDataGenerator
test_datagen = ImageDataGenerator(rescale=1./255.)
test_generator = test_datagen.flow_from_directory(
    test_dir,
    target_size=(128, 128),
    batch_size=1,
    class_mode='binary',
    shuffle=False
)

y_prob = model.predict(test_generator, test_generator.samples)
y_prob = y_prob.ravel()
y_prob

predictions  = pd.DataFrame({'y_prob': y_prob})
predictions['class'] = predictions['y_prob'].apply(lambda x: 1 if x > 0.5 else 0)
predictions

y_true = test_generator.classes
y_true

y_pred = predictions['class'].values
y_pred

test_generator.class_indices

cm = confusion_matrix(y_true, y_pred)
cm

def plot_confusion_matrix(cm):
    cm = cm[::-1]
    cm = pd.DataFrame(cm, columns=classes, index=classes[::-1])

    fig = ff.create_annotated_heatmap(z=cm.values, x=list(cm.columns), y=list(cm.index), colorscale='ice', showscale=True, reversescale=True)
    fig.update_layout(width=500, height=500, title='Confusion Matrix', font_size=16)
    fig.show()

import plotly.figure_factory as ff
plot_confusion_matrix(cm)