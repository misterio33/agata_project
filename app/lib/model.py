import os
from lib.maskJSON import MaskCreatorFromJSON
from shutil import copy

import sys
import random
import warnings

import cv2

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from tqdm import tqdm
from itertools import chain
from skimage.io import imread, imshow, imread_collection, concatenate_images
from skimage.transform import resize
from skimage.morphology import label

from keras.models import Model, load_model
from keras.layers import Input
from keras.layers.core import Dropout, Lambda
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras import backend as K

import tensorflow as tf

# Set some parameters
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNELS = 3

server = True

if server:
    TRAIN_PATH = '/CA15110_COST_Project/stage1_train/'
    TEST_PATH = '/CA15110_COST_Project/stage1_test/'
else:
    TRAIN_PATH = '/COST_Germany/agata_project/stage1_train/'
    TEST_PATH = '/COST_Germany/agata_project/stage1_test/'


class Network:

    def unet(self, pretrained_weights=None, input_size=(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS)):
        inputs = Input(input_size)
        s = Lambda(lambda x: x / 255)(inputs)

        c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(s)
        c1 = Dropout(0.1)(c1)
        c1 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c1)
        p1 = MaxPooling2D((2, 2))(c1)

        c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(p1)
        c2 = Dropout(0.1)(c2)
        c2 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c2)
        p2 = MaxPooling2D((2, 2))(c2)

        c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(p2)
        c3 = Dropout(0.2)(c3)
        c3 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c3)
        p3 = MaxPooling2D((2, 2))(c3)

        c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(p3)
        c4 = Dropout(0.2)(c4)
        c4 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c4)
        p4 = MaxPooling2D(pool_size=(2, 2))(c4)

        c5 = Conv2D(256, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(p4)
        c5 = Dropout(0.3)(c5)
        c5 = Conv2D(256, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c5)

        u6 = Conv2DTranspose(128, (2, 2), strides=(2, 2), padding='same')(c5)
        u6 = concatenate([u6, c4])
        c6 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(u6)
        c6 = Dropout(0.2)(c6)
        c6 = Conv2D(128, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c6)

        u7 = Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c6)
        u7 = concatenate([u7, c3])
        c7 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(u7)
        c7 = Dropout(0.2)(c7)
        c7 = Conv2D(64, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c7)

        u8 = Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c7)
        u8 = concatenate([u8, c2])
        c8 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(u8)
        c8 = Dropout(0.1)(c8)
        c8 = Conv2D(32, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c8)

        u9 = Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c8)
        u9 = concatenate([u9, c1], axis=3)
        c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(u9)
        c9 = Dropout(0.1)(c9)
        c9 = Conv2D(16, (3, 3), activation='elu', kernel_initializer='he_normal', padding='same')(c9)

        outputs = Conv2D(1, (1, 1), activation='sigmoid')(c9)

        model = Model(inputs=[inputs], outputs=[outputs])
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[tf.keras.metrics.MeanIoU(num_classes=2)])
        # model.summary()
        return model

        # if pretrained_weights:
        #    model.load_weights(pretrained_weights)
        #   return model

    def sort_data(self):
        data_folder = '/home/ponoprienko/CA15110_COST_Project/data/'
        train_path = TRAIN_PATH

        files = next(os.walk(data_folder))[2]

        train_id = []
        for n, id_ in tqdm(enumerate(files), total=len(files)):
            if '.png' in id_:
                id_ = id_.replace('.png', '')
                train_id.append(id_)

        for i in train_id:
            path = '/home/ponoprienko/' + train_path + i + '/images'
            os.makedirs(path)
            copy(data_folder + i + '.png', path)

            path = '/home/ponoprienko/' + train_path + i + '/masks'
            os.makedirs(path)
            a = MaskCreatorFromJSON
            a.single_json_mask(self, data_folder, i, path + '/')

    def load_data(self):

        warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
        seed = 42
        random.seed = seed
        np.random.seed = seed

        train_ids = next(os.walk('/home/ponoprienko' + TRAIN_PATH))[1]
        print(train_ids)
        test_ids = next(os.walk('/home/ponoprienko' + TEST_PATH))[1]

        # Get and resize train images and masks
        X_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        Y_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)

        sys.stdout.flush()

        for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):
            path = '/home/ponoprienko' + TRAIN_PATH + id_
            img = cv2.imread(path + '/images/' + id_ + '.png')[:, :, :IMG_CHANNELS]
            img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
            # print('img ', img.shape)
            X_train[n] = img
            mask = np.zeros((IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
            for mask_file in next(os.walk(path + '/masks/'))[2]:
                mask_ = cv2.imread(path + '/masks/' + mask_file)[:, :, 0]
                # print('m ', mask_.shape)
                mask_ = np.expand_dims(resize(mask_, (IMG_HEIGHT, IMG_WIDTH), mode='constant',
                                              preserve_range=True), axis=-1)
                mask = np.maximum(mask, mask_)
                Y_train[n] = mask
        """
        # Get and resize test images
        X_test = np.zeros((len(test_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        sizes_test = []
        print('Getting and resizing test images ... ')

        sys.stdout.flush()

        for n, id_ in tqdm(enumerate(test_ids), total=len(test_ids)):
            path = TEST_PATH + id_
            img = cv2.imread(path + '/' + id_ + '.png')[:, :, :IMG_CHANNELS]
            print('img ', img.shape)
            sizes_test.append([img.shape[0], img.shape[1]])
            img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
            print('img ', img.shape)
            X_test[n] = img
        """

        # Fit model
        model = self.unet(pretrained_weights=None, input_size=(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS))
        earlystopper = EarlyStopping(patience=5, verbose=1)
        checkpointer = ModelCheckpoint('model-dsbowl2018-1.h5', verbose=1, save_best_only=True)
        model.fit(X_train, Y_train, validation_split=0.2, batch_size=2, epochs=50,
                  callbacks=[earlystopper, checkpointer])

    def train_network(self):

        self.sort_data()
        self.load_data()