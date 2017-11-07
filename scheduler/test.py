from schema import Session

session = Session()

# Create random tasks
for i in map(str, range(10)):
  t = Task(name="testTask"+i,
           rtt=120,
           definition="echo 'hello world from task "+i+"!';")
  session.add(t)

session.commit()

# Create some nodes
for i in map(str, range(5)):
  n = Node(name="testNode"+i,
           resource="CPU=%d,RAM=%d,DISK=%d"%(randint(1,4), randint(1,4), [128,256,512,1024][randint(0,3)]),
           rtt=randint(1,14)*10,
           stats="")
  session.add(n)

session.commit()

# Create some requests
for i in range(20):
  t = session.query(Task).all()[randint(0,session.query(Task).count()-1)]
  r = TaskRequest(task_id=t.id,
      resource="CPU=%d,RAM=%d,DISK=%d"%(randint(1,4), randint(1,4), [128,256,512,1024][randint(0,3)]),
      rtt=randint(1,14)*10,
      stats="")
  session.add(r)

session.commit()

def clear_all():
  session.query(Task).delete()
  session.query(Node).delete()
  session.query(TaskRequest).delete()
  session.query(TaskStats).delete()
