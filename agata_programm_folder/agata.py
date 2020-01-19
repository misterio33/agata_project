import click
import os
import SimpleITK as sitk


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--dicompath', help='Path to folder with dicom file, for example : /home/usr/DICOM_FOLDER')
@click.option('--outputpath', help='Path to folder of converted files, for example: /home/usr/OUTPUT_FOLDER, '
                                   'if this folder does not exist, a new one will be created')
def convert(dicompath, outputpath):
    # Specify the input dicom folder path
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
            imagename = images.replace('.dcm', '')
        else:
            imagename = images
        # Reading dicom image
        img = sitk.ReadImage(folder_path + images)
        # rescale intensity range from [-1000,1000] to [0,255]
        img = sitk.IntensityWindowing(img, -1000, 1000, 0, 255)
        # convert 16-bit pixels to 8-bit
        img = sitk.Cast(img, sitk.sitkUInt8)
        # Writing converted png image
        sitk.WriteImage(img, output_folder_path + imagename + '.png')


cli = click.CommandCollection(sources=[cli1])

if __name__ == '__main__':
    cli()

