from src.schema import Session, Task, Node, TaskRequest, TaskStats
from executor.nomad_api import nomadServer, NomadJob


class Algorithm():

  def process_requests(self):
    pass


class DumbAlgorithm():

  def process_requests(self):
    session = Session()
    requests = session.query(TaskRequest).all()
    for i in requests:
      task_id = i.task_id
      task = session.query(Task).filter(id=task_id).first()
      # Query TaskStatus table and figure out if 
      # a task is being moved or not
      status = session.query(TaskStatus).filter(task_id = task_id).first()
      j = NomadJob(task.name, task.image,
                             task.cpu, task.memory)
      if status:
        #TODO: COMPLEX LOGIC!!!! 
        nomadServer.update_job(j)
      else:
        nomadServer.register_job(j)

  def reprovision(self):
    return
