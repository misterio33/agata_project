import os
#from lib.maskJSON import MaskCreatorFromJSON
from shutil import copy

import sys
import random
import warnings

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
IMG_WIDTH = 256
IMG_HEIGHT = 256
IMG_CHANNELS = 3

server = True

if server:
    TRAIN_PATH = '/CA15110_COST_Project/stage1_train/'
    TEST_PATH = '/CA15110_COST_Project/stage1_test/'
    user = '/home/ponoprienko'
else:
    TRAIN_PATH = '/COST_Germany/agata_project/app/stage1_train/'
    TEST_PATH = '/COST_Germany/agata_project/app/stage1_test/'
    user = '/home/pasha'
# /home/pasha/COST_Germany/agata_project/app/stage1_test/

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

    def mirror(self, image):
        img = cv2.imread(image)
        width = img.shape[0]  # Определяем ширину.
        height = img.shape[1]  # Определяем высоту
        new_img = np.zeros((width, height), dtype=np.uint8)
        for a in range(width):
            for b in range(height):
                new_img[a][width - b - 1] = img[a][b][0]
        return new_img

    # def sort_data(self, input_data, output_data):
    def sort_data(self):
        # data_folder = user + '/CA15110_COST_Project/data/'
        # data_folder = input_data
        data_folder = user + '/COST_Germany/agata_project/app/data/'
        # train_path = TRAIN_PATH

        files = os.listdir(data_folder)

        train_id = []
        for n, id_ in tqdm(enumerate(files), total=len(files)):
            if '.png' in id_:
                id_ = id_.replace('.png', '')
                train_id.append(id_)

        for i in train_id:

            # Creating images
            path = user + TRAIN_PATH + i + '/images'
            os.makedirs(path)
            copy(data_folder + '/' + i + '.png', path)

            path = user + TRAIN_PATH + i + 'reversed' + '/images/'
            os.makedirs(path)
            img = data_folder + '/' + i + '.png'
            img = self.mirror(img)
            cv2.imwrite(path + i + 'reversed' + '.png', img)
            #copy(data_folder + '/' + i + '.png', path)

            # Creating masks
            # /home/pasha/COST_Germany/agata_project/app/stage1_train/ +i + png
            path = user + TRAIN_PATH + i + '/masks'
            os.makedirs(path)
            a = MaskCreatorFromJSON
            a.single_json_mask(self, data_folder + '/', i, path + '/')

            img = path + '/' + i + '.png'
            path = user + TRAIN_PATH + i + 'reversed' + '/masks/'
            os.makedirs(path)

            img = self.mirror(img)
            cv2.imwrite(path + i + 'reversed' + '.png', img)

    def load_data(self, input_data, model_path):
        data_path = input_data
        model_path = model_path
        warnings.filterwarnings('ignore', category=UserWarning, module='skimage')
        seed = 42
        random.seed = seed
        np.random.seed = seed

        #train_ids = next(os.walk(user + TRAIN_PATH))[1]
        train_ids = next(os.walk(data_path))[1]
        print(train_ids)
        #test_ids = next(os.walk(user + TEST_PATH))[1]

        # Get and resize train images and masks
        X_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        Y_train = np.zeros((len(train_ids), IMG_HEIGHT, IMG_WIDTH, 1), dtype=np.bool)

        sys.stdout.flush()

        for n, id_ in tqdm(enumerate(train_ids), total=len(train_ids)):
            #path = user + TRAIN_PATH + id_
            path = data_path + '/' + id_
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
        checkpointer = ModelCheckpoint(model_path + 'model-dsbowl2018-1.h5', verbose=1, save_best_only=True)
        model.fit(X_train, Y_train, validation_split=0.2, batch_size=4, epochs=50,
                  callbacks=[earlystopper, checkpointer])

    def train_network(self, input_data, model_path):
    # def train_network(self, sort_input_data, sort_output_data):

        #self.sort_data(sort_input_data, sort_output_data)

        #self.sort_data()
        self.load_data(input_data, model_path)
