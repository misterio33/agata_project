FROM python:3

# Create app directory
COPY . /app
WORKDIR /app

# Install app dependencies
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT [ "python", "./app/agata.py" ]



