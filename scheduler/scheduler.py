import time
import threading

import schedule


def job():
  print("I'm working")


def schedule_job():
  schedule.every(10).seconds.do(job)


cease_continuous_run = threading.Event()
def run_schedule_thread():
  class ScheduleThread(threading.Thread):
    @classmethod
    def run(cls):
      while not cease_continuous_run.is_set():
        schedule.run_pending()
        time.sleep(1)

  countinuous_thread = ScheduleThread()
  countinuous_thread.start()

  return cease_continuous_run


if __name__=='__main__':
  # schedule_job()
  run_schedule_thread()
