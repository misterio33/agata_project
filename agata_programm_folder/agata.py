import click


@click.group()
def cli1():
    pass


@cli1.command()
@click.option('--dicom', '-d', help='Path to dicom file')
@click.option('--png', '-p', help='Path to folder with png')
def dicom_to_png(dicom, png):
    """Command for converting dicom files to png format"""
    print('The location of dicom file is {} , and path to folder with png is {}'.format(dicom, png))


@click.group()
def cli2():
    pass


@cli2.command()
@click.option('--dicom', '-d', help='Path to dicom file')
@click.option('--jpeg', '-j', help='Path to folder with jpeg')
def dicom_to_jpeg(dicom, jpeg):
    """Command for converting dicom files to jpeg format"""
    print('The location of dicom file is {} , and path to folder with jpeg is {}'.format(dicom, jpeg))


cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()
