import json

import nomad


class NomadSetup():
  
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.n = nomad.Nomad(host=self.ip, port=self.port)

  def get_jobs(self):
    return self.n.jobs.get_jobs()

  def register_job(self, job):
    return self.n.jobs.register_job(job.get_json())
    

class NomadJob():

  def __init__(self, name, image, CPU, memory):
    self.name = name
    self.image = image
    self.CPU = CPU
    self.memory = memory

  def get_json(self):
    with open("sample_job.json", "r") as j:
      sample = json.loads(j.read())
      sample["Job"]["ID"] = self.name
      sample["Job"]["Name"] = self.name
      tg = sample["Job"]["TaskGroups"][0]
      tg["Name"] = "taskGroup0"
      task = tg["Tasks"][0]
      task["Name"] = "task0"
      task["Config"]["image"] = self.image
      task["Resources"]["CPU"] = self.CPU
      task["Resources"]["MemoryMB"] = self.memory
      tg["Tasks"][0] = task
      sample["Job"]["TaskGroups"][0] = tg
      return json.dumps(sample)
