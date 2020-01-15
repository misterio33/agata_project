import click


@click.command()
@click.option('--dcom', '-d', help='Path to dcom file')
@click.option('--jpeg', '-j', help='Path to folder with jpeg')
def dcom_to_jpeg(dcom, jpeg):
    print('The location of dcom file is {} , and path to folder with jpeg is {}'.format(dcom, jpeg))


if __name__ == '__main__':
    dcom_to_jpeg()

