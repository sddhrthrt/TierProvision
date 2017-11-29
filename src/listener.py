import os
import sys
import threading
import time
import json

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from src.schema import TaskHistory, Session, Task

app = Flask(__name__)

@app.route("/logs", methods=["POST", ])
def logs():
  if request.method == "POST":
    data = request.get_json()
    session = Session()
    task = session.query(Task).filter(Task.name==data['app']).first()
    etc = json.dumps({k:v for k, v in data.items() if k not in ['requests', 'avg_tat', 'time']})
    hist = TaskHistory(task_id=task.id,
                       requests=data['requests'],
                       avg_tat=data['avg_tat'],
                       time=data['time'],
                       etc=etc)
    session.add(hist)
    session.commit()
    return jsonify({"STATUS": "SUCCESS"})
