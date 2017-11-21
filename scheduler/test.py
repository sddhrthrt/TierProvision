from random import randint

from schema import *

session = Session()

image = "sddhrthrt/sensorlistener:0.1.10"

def main():
  run_tests()
  #clear_all()

def run_tests():
  # Create random tasks
  for i in map(str, range(10)):
    t = Task(name="testTask"+i,
             image=image,
             latency_req=randint(1,14)*10,
             cpu=randint(1,4)*256,
             memory=randint(1,4)*256,
             expected_load=randint(1,4)*128)
    session.add(t)
    session.commit()
    tr = TaskRequest(task_id=t.id)
    session.add(tr)
    session.commit()

  # Create some nodes
  for i in map(str, range(2)):
    n = Node(name="testNode"+i,
             rtt=randint(1,3)*50,
             cpu=randint(4,8)*256,
             memory=randint(4,8)*256,
             stats="",
             ip="")
    session.add(n)
  session.commit()

def clear_all():
  session.query(TaskStats).delete()
  session.query(TaskRequest).delete()
  session.query(Task).delete()
  session.query(Node).delete()
  session.commit()

if __name__=="__main__":
  main()
