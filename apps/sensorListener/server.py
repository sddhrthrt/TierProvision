import os
import sys

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route("/ping")
def ping():
  return jsonify({"ping": "pong"})

@app.route("/upload", methods=["POST", ])
def upload_sensor_data():
  if request.method == "POST":
    data = request.get_json()
    app.logger.debug(data)
    with open(os.path.join('files/', data['filename']), 'w') as f:
      f.write(data['contents'])
    return jsonify({"filename": data['filename']})
