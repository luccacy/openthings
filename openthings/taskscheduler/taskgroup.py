'''

@author: Administrator
'''
from threading import Thread, Event, Lock, currentThread
from datetime import datetime
from openthings import aps

class NoTaskError(Exception):
    
    def __str__(self):
        return 'No task in taskgroup'

class TaskGroup(Thread):
    
    _stopped = False
    
    def __init__(self, vsensor, taskgroup_threads):
        Thread.__init__(self)
        self._vsensor = vsensor
        self._taskgroup_threads = taskgroup_threads
        self._taskgroup = []
        self._schedulering_tasks = []
        self._wakeup = Event()
        self._status = 'created'
        
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
        
        if self._taskgroup:
            self._vsensor.open()
        else:
            raise NoTaskError()
            
        while now < self.end_time and not self._stopped:
            if not self._taskgroup: 
                break
            
            for task in [task for task in self._taskgroup if task not in self._schedulering_tasks]:
                aps.add_job(task)
                self._schedulering_tasks.append(task)
            
            for task in [task for task in self._schedulering_tasks if task not in self._taskgroup]:
                aps.remove_job(task)
                self._schedulering_tasks.remove(task)
                    
            try:
                self._wakeup.wait()
            except IOError:
                pass

        self._vsensor.close()
        self.set_status('stopped')
        self._taskgroup_threads.remove(currentThread())