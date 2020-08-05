""" Name: can_writer.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging

from collections import namedtuple, OrderedDict

import can
import cantools

class CAN(object):
    signal = namedtuple(
        'signal', 'name, bytes, start_byte')

    def __init__(self):
        pass

class CANWriter(CAN):       
    def __init__(self, config):
        self._interface = config['interface']
        self._channel = config['channel']
        self._baudrate = config['baudrate']
        self._update_rate = int(config['update_rate'])
        self._bus = can.interface.Bus(self._channel, bustype=self._interface, bitrate=self._baudrate)
        self._tasks = {}

    def update(self, messages):
        ''' iterate messages, check if a task is to be created or modified 
        '''
        for name, msg in messages.items():
            task = self._tasks.get(name, None)
            if task:
                print("task found: {}".format(name))
                task.modify_data(msg)
            else:
                task = self._bus.send_periodic(msg, self._update_rate)
                self._tasks.update({name: task})

    @property
    def interface(self):
        return self._interface

    @property
    def channel(self):
        return self._channel

    @property
    def baudrate(self):
        return self._baudrate
    
    @property
    def update_rate(self):
        return self._update_rate
    
    
