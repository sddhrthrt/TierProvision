import json
import requests

import nomad


class NomadSetup():
  
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.url = "http://{}:{}/v1".format(ip, port)

  def get_jobs(self):
    res = requests.get("{}/jobs".format(self.url))
    return res.json()

  def register_job(self, job):
    res = requests.post("{}/jobs".format(self.url),
                        json=job.get_dict())
    return res.json()

  def update_job(self, job):
    res = requests.post("{}/job/{}".format(self.url, job.name),
                        json=job.get_dict())
    return res.json()

  def delete_job(self, job):
    res = requests.delete("{}/job/{}".format(self.url, job.name),
                        json=job.get_dict())
    return res.json()

nomadServer = NomadSetup("localhost", 4646)    

class NomadJob():

  def __init__(self, name, image, CPU, memory, dc):
    self.name = name
    self.image = image
    self.CPU = CPU
    self.memory = memory
    self.dc = dc

  def get_dict(self):
    with open("sample_job.json", "r") as j:
      sample = json.loads(j.read())
      sample["Job"]["ID"] = self.name
      sample["Job"]["Name"] = self.name
      sample["Job"]["Datacenters"] = [self.dc,]
      tg = sample["Job"]["TaskGroups"][0]
      tg["Name"] = "taskGroup0"
      task = tg["Tasks"][0]
      task["Name"] = "task0"
      task["Config"]["image"] = self.image
      task["Resources"]["CPU"] = self.CPU
      task["Resources"]["MemoryMB"] = self.memory
      tg["Tasks"][0] = task
      sample["Job"]["TaskGroups"][0] = tg
      return sample