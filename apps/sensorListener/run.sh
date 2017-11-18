#!/bin/bash

export FLASK_APP=server.py 
flask run -h $NOMAD_IP_HTTP -p $NOMAD_PORT_HTTP
