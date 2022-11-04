FROM python:3.10

RUN pip install pymongo

COPY receiver.py receiver.py
COPY dblibs.py dblibs.py

CMD python receiver.py --docker
