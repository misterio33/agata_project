import json
import numpy as np
import cv2
import logging
import os
import base64


class MaskCreatorFromJSON:

    # Function for creating masks and images from json file
    @staticmethod
    def create_mask(json_path, output_path, has_reflection):

        # Specify the input .dcm folder path
        # No matter does folder path has '/' at the end or not
        if json_path[-1] == '/':
            json_path = json_path
            logging.warning('Input folder is %s' % json_path)
        else:
            json_path = json_path + '/'
            logging.warning('Input folder is %s' % json_path)

        # Specify the output folder path
        # No matter whether folder path has '/' at the end or not
        if output_path[-1] == '/':
            output_path = output_path
            logging.warning('Output folder is %s' % output_path)
        else:
            output_path = output_path + '/'
            logging.warning('Output folder is %s' % output_path)

        files = os.listdir(json_path)

        training_dataset = []
        for id_file in files:
            if '.json' in id_file:
                id_file = id_file.replace('mask.json', '')
                training_dataset.append(id_file)

        for i in training_dataset:

            # Creating images
            path = output_path + i + '/images'
            os.makedirs(path)

            with open(json_path + '/' + i + 'mask.json') as f:
                data = json.load(f)

            imgdata = base64.b64decode(data['imageData'])

            filename = i
            with open(path + '/' + filename + '.png', 'wb') as f:
                f.write(imgdata)

            if has_reflection:
                path = output_path + i + '-reflection' + '/images/'
                os.makedirs(path)
                img = output_path + i + '/images/' + i + '.png'

                img = MaskCreatorFromJSON.reflection(img)
                cv2.imwrite(path + i + '-reflection' + '.png', img)

            # Creating masks
            path = output_path + i + '/masks'
            os.makedirs(path)
            MaskCreatorFromJSON.single_json_mask(json_path + '/', i, path + '/')

            if has_reflection:
                path = output_path + i + '-reflection' + '/masks/'
                os.makedirs(path)
                img = output_path + i + '/masks/' + i + '.png'
                img = MaskCreatorFromJSON.reflection(img)
                cv2.imwrite(path + i + '-reflection' + '.png', img)

    # Function for creating mask from json file
    @staticmethod
    def single_json_mask(data_folder, json_file_id, output_path):
        with open(data_folder + json_file_id + 'mask' + '.json') as f:
            data = json.load(f)

            # Reading image parameters
            img_height = data['imageHeight']
            img_width = data['imageWidth']

            # Creating black background
            img = np.zeros((img_height, img_width), dtype="uint8")

            # Making masks for left and right regions of interest
            for mask_part in range(0, len(data['shapes'])):
                points = data['shapes'][mask_part]['points']
                points = np.array(points, np.int32)
                img = cv2.fillPoly(img, [points], 255)

            # Saving created mask
            cv2.imwrite(output_path + json_file_id + '.png', img)

    # Function for reflection image
    @staticmethod
    def reflection(image):
        img = cv2.imread(image)
        width = img.shape[0]
        height = img.shape[1]
        new_img = np.zeros((width, height), dtype=np.uint8)
        for a in range(width):
            for b in range(height):
                new_img[a][width - b - 1] = img[a][b][0]
        return new_img



