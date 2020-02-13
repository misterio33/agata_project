import json
import numpy as np
import cv2
import logging
import os


class MaskCreatorFromJSON:

    def mask_from_json(self, json_path, output_path):

        # Specify the input .dcm folder path
        # No matter does folder path has '/' at the end or not
        if json_path[-1] == '/':
            folder_path = json_path
            logging.warning('Input folder is %s' % json_path)
        else:
            folder_path = json_path + '/'
            logging.warning('Input folder is %s' % json_path)

        # Specify the output folder path
        # No matter whether folder path has '/' at the end or not
        if output_path[-1] == '/':
            output_folder_path = output_path
            logging.warning('Converted files will be at this location %s' % output_path)
        else:
            output_folder_path = output_path + '/'
            logging.warning('Converted files will be at this location %s' % output_path)

        # Creating new output directory if it does not exist
        if not os.path.exists(output_folder_path):
            os.makedirs(output_folder_path)
            logging.warning('Converted files will be at this location %s' % output_path)

        images_path = os.listdir(folder_path)

        for n, file in enumerate(images_path):
            # reading JSON file
            with open(folder_path + file) as f:
                data = json.load(f)

            # Deleting '.json' from file name
            if '.json' in file:
                image_name = file.replace('.json', '')
            else:
                image_name = file

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
            cv2.imwrite(output_folder_path + image_name + '.png', img)



