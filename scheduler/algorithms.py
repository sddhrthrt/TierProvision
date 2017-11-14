from src.schema import Session, Task, Node, TaskRequest, TaskStats


class Algorithm():

  def process_requests(self):
    pass


class DumbAlgorithm():

  def process_requests(self):
    session = Session()
    requests = session.query(TaskRequest).all()
    for i in requests:
      print(i)

  def reprovision(self):
    return
