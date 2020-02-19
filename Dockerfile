FROM python:3

# Create app directory
COPY . /app
WORKDIR /app

# Install app dependencies
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-2.1.0-cp37-cp37m-manylinux2010_x86_64.whl
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT [ "python", "./app/agata.py" ]



