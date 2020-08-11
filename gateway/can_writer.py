""" Name: can_writer.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging

from collections import namedtuple, OrderedDict

import can
import cantools

class CANWriter(object):       
    def __init__(self, config):
        self._interface = config['interface']
        self._channel = config['channel']
        self._baudrate = config['baudrate']
        self._update_rate = float(config['update_rate'])
        self._bus = can.interface.Bus(self._channel, bustype=self._interface, bitrate=self._baudrate)
        self._tasks = {}

    def publish(self, name, msg):
        ''' iterate messages, check if a task is to be created or modified 
        '''
        task = self._tasks.get(name, None)
        if task:
            print("task found: {}".format(name))
            task.modify_data(msg)
        else:
            task = self._bus.send_periodic(msg, self._update_rate)
            self._tasks.update({name: task})

    def stop(self):
        for task in self._tasks.values():
            task.stop()

