import click
from lib.dicom import DicomConverter
from lib.maskJSON import MaskCreatorFromJSON


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


@click.group()
def cli2():
    pass


@cli2.command()
@click.option('--json_path', help='Name of json file, it must be at the same location as agata.py'
                                  '(temporally, will be changed soon)')
@click.option('--output_path', help='Path to folder of converted files, for example: /home/usr/OUTPUT_FOLDER, '
                                    'if this folder does not exist, a new one will be created')
def jsonmask(json_path, output_path):
    json = MaskCreatorFromJSON()
    json.mask_from_json(json_path, output_path)


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
