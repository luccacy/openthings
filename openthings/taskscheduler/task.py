'''
Created on 2014-5-26

@author: zhouyu
'''
import os


class Task():
    
    def __init__(self, name):
        self._name = name
        
    def __str__(self):
        return '%s' % self._name