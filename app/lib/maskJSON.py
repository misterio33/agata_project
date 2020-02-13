import json
import numpy as np
import cv2


class MaskCreatorFromJSON:

    @staticmethod
    def mask_from_json(file):
        # reading JSON file
        with open(file) as f:
            data = json.load(f)

        # Reading image parameters
        image_name = file.replace('.json', '')
        img_height = data['imageHeight']
        img_width = data['imageWidth']

        # Creating black background
        img = np.zeros((img_height, img_width), dtype="uint8")

        # Making masks for left and right regions of interest
        for mask_part in range(0, len(data['shapes'])):
            points = data['shapes'][mask_part]['points']
            points = np.array(points, np.int32)
            img = cv2.fillPoly(img, [points], 255)
        cv2.imwrite(image_name + ".png", img)