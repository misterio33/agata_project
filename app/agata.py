import click
from lib.dicom import DicomConverter
#from lib.maskJSON import MaskCreatorFromJSON
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
@click.option('--input_data', help='Path to folder with data such as pictures and masks')
@click.option('--model_path', help='Path to folder with model')
#@click.option('--test_data', help='Path to folder with test data')
#@click.option('--pretrained_model', help='If you have pretrained model, please write the name of this model'
 #                                        '(model must be at the same place as agata.py), if not - print "None"')
#def Unet(sort_input_data, sort_output_data):
def unet(input_data, model_path):
    model = Network()
    model.train_network(input_data, model_path)


cli = click.CommandCollection(sources=[cli1, cli2, cli3])

if __name__ == '__main__':
    cli()
