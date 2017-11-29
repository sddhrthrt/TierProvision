import os
import sys
import threading
import time

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename


app = Flask(__name__)

cpu_busy_end = int(time.time())
memory_busy_end = int(time.time())
target_memory_size = 0
big_string = None

logs = {
    "requests": {
        "request_cpu": 0,
        "request_memory": 0
      },
    "uplink": {
        "avg": 0
      },
    "downlink": {
        "avg": 0
      },
    "power": {
        "rem": 100
      }
  }

class CPUThread(threading.Thread):
  @classmethod
  def run(cls):
    while True:
      if int(time.time()) < cpu_busy_end:
        r = 213123
        r * r
        r = r + 1
      else:
        time.sleep(1)

cpu_thread = CPUThread()
cpu_thread.start()

class MemoryThread(threading.Thread):
  @classmethod
  def run(cls):
    while True:
      if int(time.time()) < memory_busy_end:
        big_string = ' '*target_memory_size*100000
      else:
        big_string = None
        time.sleep(1)

memory_thread = MemoryThread()
memory_thread.start()


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

@app.route("/busy/cpu", methods=["POST", ])
def keep_cpu_busy():
  global cpu_busy_end
  global logs
  if request.method == "POST":
    logs["requests"]["cpu"] += 1
    data = request.get_json()
    t = data["time"]
    cpu_busy_end = int(time.time())+t
    return jsonify({"cpu_busy_until": cpu_busy_end})


@app.route("/busy/memory", methods=["POST", ])
def keep_memory_busy():
  global memory_busy_end
  global target_memory_size
  global logs
  if request.method == "POST":
    logs["requests"]["memory"] += 1
    data = request.get_json()
    t = data["time"]
    m = data["memory"]
    memory_busy_end = int(time.time())+t
    target_memory_size = m
    return jsonify({"memory_busy_until": memory_busy_end,
                    "target_memory_size": target_memory_size})

@app.route("/logs", methods=["GET", ])
def get_logs():
  if request.method == "GET":
    return jsonify(logs)
