# Base the image on python 3.10
FROM python:3.10

# Install dependencies
RUN pip install pymongo

# Copy over all the files
COPY . .

# Start receiver with docker flag on startup
CMD python receiver.py --docker
