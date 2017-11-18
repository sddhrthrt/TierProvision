FROM python:3.6.3

RUN mkdir /app
ADD server.py /app/server.py
ADD requirements.txt /app/requirements.txt
ADD run.sh /app/run.sh
RUN mkdir /app/files

WORKDIR /app
RUN pip install -r requirements.txt
ENV FLASK_APP server.py

ENTRYPOINT ["/bin/bash", "/app/run.sh"]

