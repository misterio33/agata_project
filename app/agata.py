import click
import os
import SimpleITK as sitk


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--dicompath', help='Path to folder with .dcm files, for example : /home/usr/DICOM_FOLDER')
@click.option('--outputpath', help='Path to folder of converted files, for example: /home/usr/OUTPUT_FOLDER, '
                                   'if this folder does not exist, a new one will be created')
def convert(dicompath, outputpath):
    window_minimum = -2000
    window_maximum = 2000
    output_minimum = 0
    output_maximum = 255
    # Specify the input .dcm folder path
    # No matter does folder path has '/' at the end or not
    if dicompath[-1] == '/':
        folder_path = dicompath
    else:
        folder_path = dicompath + '/'

    # Specify the output folder path
    # No matter does folder path has '/' at the end or not
    if outputpath[-1] == '/':
        output_folder_path = outputpath
    else:
        output_folder_path = outputpath + '/'

    # Creating new output directory if not exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    images_path = os.listdir(folder_path)
    for n, images in enumerate(images_path):
        # Deleting '.dcm' from file name
        if '.dcm' in images:
            image_name = images.replace('.dcm', '')
        else:
            image_name = images
            
        # Reading .dcm image
        img = sitk.ReadImage(folder_path + images)

        # rescale intensity range from [-2000,2000] to [0,255]
        img = sitk.IntensityWindowing(img, window_minimum, window_maximum, output_minimum, output_maximum)

        # convert 16-bit pixels to 8-bit
        img = sitk.Cast(img, sitk.sitkUInt8)
        # Writing converted png image
        sitk.WriteImage(img, output_folder_path + image_name + '.png')


cli = click.CommandCollection(sources=[cli1])

if __name__ == '__main__':
    cli()

