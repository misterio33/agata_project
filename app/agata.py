import click
from lib.dicom import DicomConverter

@click.group()
def cli1():
    pass

@cli1.command()
@click.option('--dicom_path', help='Path to folder with .dcm files, for example : /home/usr/DICOM_FOLDER')
@click.option('--output_path', help='Path to folder of converted files, for example: /home/usr/OUTPUT_FOLDER, '
                                    'if this folder does not exist, a new one will be created')
def convert(dicom_path, output_path):
    dicom = DicomConverter()
    dicom.convert(dicom_path, output_path)

cli = click.CommandCollection(sources=[cli1])

if __name__ == '__main__':
    cli()