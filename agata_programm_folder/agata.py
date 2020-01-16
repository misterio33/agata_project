import click
import pydicom
import os
import cv2


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--dicompath', help='Path to folder with dicom file, for example : /home/usr/DICOM_TEST/')
@click.option('--outputpath', help='Path to folder of converted files, for example: /home/usr/OUTPUT/')
@click.option('--converttype', help='Select output type file, choose from png or jpg')
def dicomconvert(dicompath, outputpath, converttype):
    """Command for converting dicom files to jpeg/png format"""
    print('The location of folder with dicom files is {}'.format(dicompath))
    print('The location of folder with png files is {}'.format(outputpath))
    input_dir = dicompath
    out_dir = outputpath
    out_put_type = converttype

    dicom_files_list = [file for file in os.listdir(input_dir)]

    for file in dicom_files_list:
        ds = pydicom.read_file(input_dir + file)  # read dicom image
        image = ds.pixel_array  # get image array
        if out_put_type == 'png':
            cv2.imwrite(out_dir + file.replace('.dcm', '.png'), image)  # write png image
            print(file + ' was converted to png')
        elif out_put_type == 'jpg':
            cv2.imwrite(out_dir + file.replace('.dcm', '.jpg'), image)  # write jpg image
            print(file + ' was converted to jpg')
        else:
            print('select correct type')
            break

    print('Was converted ' + str(len(dicom_files_list)) + ' files')


cli = click.CommandCollection(sources=[cli1])

if __name__ == '__main__':
    cli()

