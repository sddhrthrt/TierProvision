FROM python:3.6.3

RUN mkdir /app
ADD requirements.txt /app/requirements.txt
RUN mkdir /app/files

WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP server.py

ADD server.py /app/server.py
ADD run.sh /app/run.sh

ENTRYPOINT ["/bin/bash", "/app/run.sh"]

