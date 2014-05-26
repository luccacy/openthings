'''
Created on 2014-5-26

@author: zhouyu
'''
from openthings.taskscheduler.scheduler import Scheduler
from openthings.taskscheduler.task import Task
import time

if __name__ == '__main__':
    
    sched = Scheduler()
    
    
    print 'main'
    task = Task('task0')
    print task
    sched.add_task('taskgroup0', task)
    sched.start()
    task = Task('task1')
    print task
    sched.add_task('taskgroup0', task)
    
    print 'ok'
    while True:
        print 'main'
        time.sleep(1)