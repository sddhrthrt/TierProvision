import logging

logger = logging.getLogger(__name__)

class Monitor():

  def monitor(self):
    pass


class DumbMonitor(Monitor):

  def monitor(self):
    session = Session()
    nodes = session.query(Node).all()
    stats = {
        1: "CPU_AVG:24;MEM_AVG:35;POWER_REM:40",
        2: "CPU_AVG:45;MEM_AVG:80;POWER_REM:80"
        }
    for i in nodes:
      ip = i.ip
      # wont actually fetch  
      ip.stats = stats[i.id]
      session.add(i)
      session.save()
    
    apps = session.query(Task).all()
    
class NomadMonitor(Monitor):
  @override
  def monitor(self):
    session = Session()
    nomad = NomadSetup("localhost", 4646)
    ts = session.query(TaskStatus).all()
    for task in ts:

