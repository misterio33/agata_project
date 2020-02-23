import click
from lib.dicom import DicomConverter
from lib.maskJSON import MaskCreatorFromJSON
from lib.model import Network


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
@click.option('--json_path', help='Path to folder with .json files, for example : /home/usr/JSON_FOLDER')
@click.option('--output_path', help='Path to folder of converted files, for example: /home/usr/OUTPUT_FOLDER, '
                                    'if this folder does not exist, a new one will be created')
def jsonmask(json_path, output_path):
    json = MaskCreatorFromJSON()
    json.mask_from_json(json_path, output_path)


@click.group()
def cli3():
    pass


@cli3.command()
@click.option('--json_path', help='absolute path to folder with labelme json files')
@click.option('--output_path', help='absolute path to output folder with images and masks')
@click.option('--has_reflection', help='Print True if you need reflect your image')
def create_mask(json_path, output_path, has_reflection):
    MaskCreatorFromJSON.create_mask(json_path, output_path, has_reflection)


@click.group()
def cli4():
    pass


@cli4.command()
@click.option('--input_data', help='Absolute file path to training folder with images and masks')
@click.option('--model_name', help='Indicates filename of model')
@click.option('--model_path', help='Absolute file path to models folder')
@click.option('--batch_size', help='Indicates Batch Size')
@click.option('--epochs', help='Indicates how many epochs will be used during training')
@click.option('--validation_split', help='indicates validation split')
def unet_create_model(input_data, model_name, model_path, batch_size, epochs, validation_split):
    model = Network()
    model.train_network(input_data, model_name, model_path, batch_size, epochs, validation_split)


cli = click.CommandCollection(sources=[cli1, cli2, cli3, cli4])

if __name__ == '__main__':
    cli()
