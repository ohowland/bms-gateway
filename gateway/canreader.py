""" Name: can_reader.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging

import can
import cantools

class CANReader(object):       
    def __init__(self, config, loop=None):
        self._interface = config['interface']
        self._channel = config['channel']
        self._baudrate = config['baudrate']
        self._update_rate = float(config['update_rate'])
        self._bus = can.interface.Bus(self._channel,
                                      bustype=self._interface, 
                                      bitrate=self._baudrate)
        self._listener = can.AsyncBufferedReader()
        self._notifier = can.Notifier(self._bus, 
                                      [self._listener], 
                                      loop=loop)

    def __iter__(self):
        return self

    async def __next__(self):
        msg = await self._listener.get_message()
        if msg:
            print(msg)
            return msg
        else:
            raise StopIteration

    async def get_message(self):
        msg = await self._listener.get_message()
        return msg

    def stop(self):
        self._notifer.stop()

    @property
    def interface(self):
        return self._interface

    @property
    def channel(self):
        return self._channel

    @property
    def baudrate(self):
        return self._baudrate


