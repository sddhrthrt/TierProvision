FROM python:3.6.3

ADD server.py /server.py
ADD requirements.txt /requirements.txt
RUN mkdir /files

RUN pip install -r requirements.txt
ENV FLASK_APP server.py
EXPOSE 5000

ENTRYPOINT ["flask", "run", "-h", "0.0.0.0", "-p", "$NOMAD_PORT_HTTP"]

