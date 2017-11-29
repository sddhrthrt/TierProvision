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
    "rtt_avg": {
      "api_memory": 0,
      "api_cpu": 0,
      "api_network": 0
      },
    "request_count": {
      "api_memory": 0,
      "api_cpu": 0,
      "api_network": 0
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


def update_logs(api, rtt):
  global logs
  request_count = logs["request_count"][api]
  rtt_avg = logs["rtt_avg"][api]
  new_rtt_avg = (rtt_avg*request_count + rtt)/(request_count+1)
  request_count += 1
  logs["request_count"][api] = request_count
  logs["rtt_avg"][api] = new_rtt_avg


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
  tick = int(round(time.time()*1000))
  global cpu_busy_end
  if request.method == "POST":
    data = request.get_json()
    t = data["time"]
    cpu_busy_end = int(time.time())+t
    tock = int(round(time.time()*1000))
    update_logs("api_cpu", tock-tick)
    return jsonify({"cpu_busy_until": cpu_busy_end})


@app.route("/busy/memory", methods=["POST", ])
def keep_memory_busy():
  tick = int(round(time.time()*1000))
  global memory_busy_end
  global target_memory_size
  if request.method == "POST":
    data = request.get_json()
    t = data["time"]
    m = data["memory"]
    memory_busy_end = int(time.time())+t
    target_memory_size = m
    tock = int(round(time.time()*1000))
    update_logs("api_cpu", tock-tick)
    return jsonify({"memory_busy_until": memory_busy_end,
                    "target_memory_size": target_memory_size})


@app.route("/load/network", methods=["POST", ])
def load_network():
  tick = int(round(time.time()*1000))
  if request.method == "POST":
    n = data["n"]
    for i in range(int(n)):
      f = request.get("http://apache.forsale.plus/spark/spark-2.2.0/spark-2.2.0-bin-hadoop2.7.tgz")
      with open("randfile", "wb") as fo:
        fo.write(f.content)
    tock = int(round(time.time()*1000))
    update_logs("api_network", tock-tick)
    return jsonify({"n": n})

@app.route("/logs", methods=["GET", ])
def get_logs():
  if request.method == "GET":
    return jsonify(logs)
