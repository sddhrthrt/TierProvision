import datetime

from sqlalchemy import create_engine, Column, Integer, String, \
    ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://tierprovision:tierprovision@localhost/scheduler')
Base = declarative_base()

Session = sessionmaker(bind=engine)

class Task(Base):
  __tablename__ = 'task'

  id = Column(Integer, primary_key=True)
  name = Column(String(128))
  image = Column(String(1024))
  latency_req = Column(Integer)
  cpu = Column(Integer)
  memory = Column(Integer)
  storage = Column(Integer)
  uplink = Column(Integer)
  downlink = Column(Integer)
  expected_load = Column(String(1024))

  def __repr__(self):
    return "<Task(id='%s', name='%s)>" % (
        self.id, self.name)

class Node(Base):
  __tablename__ = 'node'

  id = Column(Integer, primary_key=True)
  name = Column(String(128))
  rtt = Column(Integer)
  cpu = Column(Integer)
  memory = Column(Integer)
  storage = Column(Integer)
  stats = Column(String(1024))
  uplink = Column(Integer)
  downlink = Column(Integer)
  ip = Column(String(1024))
  
  def __repr__(self):
    return "<Node(id='%s', name='%s')>" % (
        self.id, self.name)

class TaskRequest(Base):
  __tablename__ = 'task_request'

  id = Column(Integer, primary_key=True)
  task_id = Column(Integer, ForeignKey('task.id'))
  timestamp = Column(DateTime, default=datetime.datetime.utcnow)
  
  def __repr__(self):
    return "<TaskRequest(id='%s', task_id='%s')>" % (
        self.id, self.task_id)

class TaskStats(Base):
  __tablename__ = 'task_stats'

  id = Column(Integer, primary_key=True)
  task_id = Column(Integer, ForeignKey('task.id'))
  cpu = Column(Integer)
  memory = Column(Integer)
  provision_time = Column(DateTime, default=datetime.datetime.utcnow)
  node_id = Column(Integer, ForeignKey('node.id'))
  avg_rtt = Column(Integer)
  avg_resource = Column(String(128))
  avg_load = Column(Integer)
  avg_uplink = Column(Integer)
  avg_downlink = Column(Integer)
  
  def __repr__(self):
    return "<TaskStats(id='%s', task_id='%s')>" % (
        self.id, self.task_id)

class TaskHistory(Base):
  __tablename__ = 'task_history'

  id = Column(Integer, primary_key=True)
  task_id = Column(Integer, ForeignKey('task.id'))
  requests = Column(Integer)
  avg_tat = Column(Integer)
  time = Column(DateTime)
  etc = Column(String(1024))

if __name__ == '__main__':
  Base.metadata.create_all(engine)
