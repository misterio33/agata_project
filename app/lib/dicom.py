import os
import SimpleITK as sitk
import logging

# Defining constants:
WINDOW_MINIMUM = -2048
WINDOW_MAXIMUM = 2047
OUTPUT_MINIMUM = 0
OUTPUT_MAXIMUM = 255

class DicomConverter:
  def convert(self, dicom_path, output_path):
    # Specify the input .dcm folder path
    # No matter does folder path has '/' at the end or not
    if dicom_path[-1] == '/':
        folder_path = dicom_path
        logging.warning('Input folder is %s' % dicom_path)
    else:
        folder_path = dicom_path + '/'
        logging.warning('Input folder is %s' % dicom_path)

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
    logging.warning('Starting converting')
    counter = 0
    for n, images in enumerate(images_path):
        try:
            counter = counter + 1
            # Deleting '.dcm' from file name
            if '.dcm' in images:
                image_name = images.replace('.dcm', '')
            else:
                image_name = images

            # Reading .dcm image
            img = sitk.ReadImage(folder_path + images)

            # rescale intensity range from [-2048,2047] to [0,255]
            img = sitk.IntensityWindowing(img, WINDOW_MINIMUM, WINDOW_MAXIMUM, OUTPUT_MINIMUM, OUTPUT_MAXIMUM)

            # convert 11-bit pixels to 8-bit
            img = sitk.Cast(img, sitk.sitkUInt8)
            # Writing converted png image
            sitk.WriteImage(img, output_folder_path + image_name + '.png')
            logging.warning('File %s has been converted to png' % image_name)
        except Exception as ex:
            logging.error(ex)
    logging.warning('%s file(s) has(ve) been converted from .dcm to  .png' % counter)
