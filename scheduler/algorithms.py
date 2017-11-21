from src.schema import Session, Task, Node, TaskRequest, TaskStats
from executor.nomad_api import nomadServer, NomadJob
import logging

logger = logging.getLogger(__name)

class Algorithm():

  def process_requests(self):
    pass


class DumbAlgorithm(Algorithm):

  def process_requests(self):
    session = Session()
    requests = session.query(TaskRequest).all()
    for i in requests:
      logger.debug("Processing request: %s", i)
      task_id = i.task_id
      task = session.query(Task).filter(id=task_id).first()
      # Query TaskStatus table and figure out if 
      # a task is being moved or not
      status = session.query(TaskStatus).filter(task_id = task_id).first()
      j = NomadJob(task.name, task.image,
                             task.cpu, task.memory)
      if status:
        #TODO: COMPLEX LOGIC!!!! 
        logger.debug("Updating job: %s", j)
        nomadServer.update_job(j)
      else:
        logger.debug("Creating job: %s", j)
        nomadServer.register_job(j)

  def reprovision(self):
    return


class DestructionAlgorithm(Algorithm):

  def process_requests(self):
    session = Session()
    tasks = session.query(Task).all()
    for task in tasks:
      j = NomadJob(task.name, task.image,
                             task.cpu, task.memory)
      logger.debug("Deleting job: %s", j)
      nomadServer.delete_job(j)
