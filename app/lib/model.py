import os
from lib.maskJSON import MaskCreatorFromJSON
from shutil import copy

import sys
import random
import warnings
import logging

import cv2

import numpy as np


from tqdm import tqdm

from skimage.transform import resize


from keras.models import Model, load_model
from keras.layers import Input
from keras.layers.core import Dropout, Lambda
from keras.layers.convolutional import Conv2D, Conv2DTranspose
from keras.layers.pooling import MaxPooling2D
from keras.layers.merge import concatenate
from keras.callbacks import EarlyStopping, ModelCheckpoint


import tensorflow as tf

# Set some parameters
IMG_WIDTH = 128
IMG_HEIGHT = 128
IMG_CHANNELS = 3


class Network:

    @staticmethod
    def unet(input_size=(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS)):
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

        return model

    @staticmethod
    def train_network(input_data, model_name, model_path, batch_size, epochs, validation_split):

        # Specify the output model folder
        # No matter does folder path has '/' at the end or not
        if model_path[-1] == '/':
            model_path = model_path
            logging.warning('Input folder is %s' % model_path)
        else:
            model_path = model_path + '/'
            logging.warning('Input folder is %s' % model_path)

        data_path = input_data
        warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
        seed = 42
        random.seed = seed
        np.random.seed = seed

        logging.warning('data_path: %s' % data_path)
        logging.warning('model_path: %s' % model_path)

        train_ids = next(os.walk(data_path))[1]
        print(train_ids)

        # Get and resize train images and masks
        train_images = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        train_masks = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)

        sys.stdout.flush()

        for n, id_image in tqdm(enumerate(train_ids), total=len(train_ids)):
            path = data_path + '/' + id_image
            img = cv2.imread(path + '/images/' + id_image + '.png')[:, :, :IMG_CHANNELS]
            img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)

            train_images[n] = img
            mask = np.zeros((IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)
            for mask_file in next(os.walk(path + '/masks/'))[2]:
                mask_polygon = cv2.imread(path + '/masks/' + mask_file)[:, :, 0]

                mask_polygon = np.expand_dims(resize(mask_polygon, (IMG_HEIGHT, IMG_WIDTH), mode='constant',
                                              preserve_range=True), axis=-1)
                mask = np.maximum(mask, mask_polygon)
                train_masks[n] = mask

        # Fit model
        model = Network.unet(input_size=(IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS))
        earlystopper = EarlyStopping(patience=5, verbose=1)
        checkpointer = ModelCheckpoint(model_path + model_name + '.h5', verbose=1, save_best_only=True)
        model.fit(train_images, train_masks, validation_split=float(validation_split), batch_size=int(batch_size), epochs=int(epochs),
                  callbacks=[earlystopper, checkpointer])

    @staticmethod
    def make_prediction(model_name, model_path, test_path):

        # Specify the model folder directory
        # No matter does folder path has '/' at the end or not
        if model_path[-1] == '/':
            model_path = model_path
            logging.warning('Model path is %s' % model_path)
        else:
            model_path = model_path + '/'
            logging.warning('Model path is %s' % model_path)

        # Specify the test images folder
        # No matter does folder path has '/' at the end or not
        if test_path[-1] == '/':
            test_path = test_path
            logging.warning('Test images folder is %s' % test_path)
        else:
            test_path = test_path + '/'
            logging.warning('Test images folder is %s' % test_path)

        test_ids = next(os.walk(test_path))[1]
        logging.warning("test_ids %s" % test_ids)
        test_ids, len(test_ids)
        test_images = np.zeros((len(test_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        sizes_test = []
        print('Getting and resizing test images ... ')
        sys.stdout.flush()
        for n, id_image in tqdm(enumerate(test_ids), total=len(test_ids)):
            path = test_path + id_image + '/images/' + id_image + '.png'
            print(path)
            img = cv2.imread(path)[:, :, :IMG_CHANNELS]
            print('img ', img.shape)
            sizes_test.append([img.shape[0], img.shape[1]])
            img = resize(img, (IMG_HEIGHT, IMG_WIDTH), mode='constant', preserve_range=True)
            print('img ', img.shape)
            test_images[n] = img

        model_save_name = model_path + '/' + model_name
        model = tf.keras.models.load_model(model_save_name)
        preds_test = model.predict(test_images, verbose=1)
        preds_test_t = (preds_test > 0.5).astype(np.uint8)

        model_name = model_name.replace('.h5', '/')
        os.makedirs(model_path + model_name + 'predictions')

        for predicted_images in range(len(test_ids)):
            prediction = np.squeeze(preds_test_t[predicted_images] * 255)
            pred_name = test_ids[predicted_images]
            image_name = (model_path + model_name + 'predictions/' + pred_name + '.png')
            logging.warning(image_name)
            cv2.imwrite(image_name, prediction)


