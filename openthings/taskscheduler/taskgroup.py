'''

@author: Administrator
'''
from threading import Thread, Event, Lock, currentThread
from datetime import datetime
from openthings import aps
import time

class NoTaskError(Exception):
    
    def __str__(self):
        return 'No task in taskgroup'

class TaskGroup(Thread):
    
    _stopped = False
    
    def __init__(self, name, vsensor, taskgroup_threads):
        Thread.__init__(self)
        self._name = name
        self._vsensor = vsensor
        self._taskgroup_threads = taskgroup_threads
        self._taskgroup = []
        self._schedulering_tasks = []
        self._wakeup = Event()
        self._status = 'created'
    
    def __str__(self):
        return '%s' % self._name
        
    def add_task(self, task):
        self._taskgroup.append(task)
        self._wakeup.set()
        
    def del_task(self, task):
        self._taskgroup.remove(task)
        self._wakeup.set()
        
    def set_status(self, status):
        self._status = status
        
    def get_status(self):
        return self._status
    
    def stop(self):
        self._stopped = True
        self._wakeup.set()

    def get_end_time(self):
        end_time = None
        return end_time
    
    def run(self):
        
        self.set_status('running')
        now = datetime.now()
        
#         if self._taskgroup:
#             self._vsensor.open()
#         else:
#             raise NoTaskError
        self._wakeup.clear()
        while not self._stopped:
            print '===taskgroup : %s' % self._taskgroup
            if not self._taskgroup: 
                break
            print '------after break'
            for task in [task for task in self._taskgroup if task not in self._schedulering_tasks]:
#                 aps.add_job(task)
                print '+++task: %s' % task
                self._schedulering_tasks.append(task)
            
            for task in [task for task in self._schedulering_tasks if task not in self._taskgroup]:
#                 aps.remove_job(task)
                print task
                self._schedulering_tasks.remove(task)
                    
            try:
                self._wakeup.wait()
            except IOError:
                pass
            self._wakeup.clear()
            time.sleep(1)
# 
#         self._vsensor.close()
        self.set_status('stopped')
        self._taskgroup_threads.pop(currentThread())