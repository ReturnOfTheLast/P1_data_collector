FROM python:3.10

RUN pip install pymongo

COPY . .

CMD python receiver.py --docker
