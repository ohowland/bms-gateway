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
        self._update_rate = config['update_rate']
        self._bus = can.interface.Bus(self._channel, bustype=self._interface, bitrate=self._baudrate)
        self._tasks = {}

    def update(self, msgs):
        for name, msg in msgs.items():
            task = self._tasks.get(name, None)
            if task:
                print("task found: {}".format(name))
                task.modify_data(msg)
            else:
                print("Creating new task: {}".format(name))
                
                task = self._bus.send_periodic(msg, 0.2)
                self._tasks.update({name: task})
