'''

@author: Administrator
'''
from threading import Thread, Event, Lock
from datetime import datetime, timedelta
from openthings.common.timeutils import *

from logging import getLogger
LOG = getLogger(__name__)

class AlreadyRunningError(Exception):
    """
    Raise exception when the task scheduler is already running
    """

    def __str__(self):
        return 'Task scheduler is already running'
    
class Scheduler():
    
    _thread = None
    _stopped = False
    
    def __init__(self):
        """
        Initialize task scheduler
        """
        self._wakeup = Event()
        self._taskstore = {} 
        self._taskgroup_threads = {}
        self._pending_tasks = {}
        self._taskstore_lock = Lock()
    
    def start(self):
        pass
    
    def shutdown(self):
        pass
    
    def add_taskgroup(self, taskgroup_name):
        self._taskstore_lock.acquire()
        try:
            if taskgroup_name in self._taskstore:
                raise KeyError('Taskgroup "%s" is already in use' % taskgroup_name)
            taskgroup = []
            self._taskstore[taskgroup_name] = taskgroup
        finally:
            self._taskstore_lock.release()
        
    def del_taskgroup(self, taskgroup_name):    
        self._taskstore_lock.acquire()
        try:
            if taskgroup_name not in self._taskstore:
                raise KeyError('No such taskgroup "%s" ' % taskgroup_name)
            taskgroup = self._taskstore.pop(taskgroup_name)
        finally:
            self._taskstore_lock.release()
        
        
    def add_task(self, taskgroup_name, task):
        """
        taskgroup_name: task list to store tasks belongs to the same type
        task: the speciled task 
        """
        self._taskstore_lock.acquire()
        taskgroup = self._taskstore.get(taskgroup_name, None)
        if taskgroup is  None:
            self.add_taskgroup(taskgroup_name)
            
        taskgroup.append(task)
        self._taskstore_lock.release()
        
        self._wakeup.set()
    
    def del_task(self, taskgroup_name, task):
        self._taskstore_lock.acquire()
        taskgroup = self._taskstore.get(taskgroup_name, None)
        if taskgroup is  None:
            raise KeyError('No such taskgroup "%s"' % taskgroup_name)
            
        taskgroup.remove(task)
        self._taskstore_lock.release()
    
    def update_task(self):
        pass
    
    def get_task(self):
        pass
    
    def get_tasks(self):
        pass
    
    def _process_tasks(self, now):
        """
        Iterates through jobs in every jobstore, starts pending jobs
        and figures out the next wakeup time.
        """
        next_wakeup_time = None
        self._jobstores_lock.acquire()
        try:
            for taskgroup_name, taskgroup in self._taskstore.iteritems():
                taskgroup.start()
                self._taskgroup_threads[taskgroup_name]['status'] = 'running'
        
        
    
    
    
    def _main_loop(self):
        """
        main loop to execute tasks
        """
        LOG.info("Task scheduler started")
        self._wakeup.clear()
        
        while not self._stopped:
            now = datetime.now()
            next_wakeup_time = self._process_tasks(now)
            
            if next_wakeup_time is not None:
                """fix me to get wait_seconds"""
                wait_seconds = time_difference(next_wakeup_time, now)
                LOG.debug('Next wakeup is due at %s (in %f seconds)',
                             next_wakeup_time, wait_seconds)
                try:
                    self._wakeup.wait(wait_seconds)
                except IOError:  # Catch errno 514 on some Linux kernels
                    pass
                self._wakeup.clear()
            else:
                LOG.debug('No jobs; waiting until a job is added')
                try:
                    self._wakeup.wait()
                except IOError:  # Catch errno 514 on some Linux kernels
                    pass
                self._wakeup.clear()
    