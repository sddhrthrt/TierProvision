#!/bin/bash

export FLASK_APP=server.py 
flask run -h 0.0.0.0 -p $NOMAD_PORT_http
