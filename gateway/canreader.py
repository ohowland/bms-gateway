""" Name: can_reader.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging

import can
import cantools

log = logging.getLogger('can_reader')

class CANReader(object):       
    def __init__(self, config, bus, loop):
        self._listener = can.AsyncBufferedReader()
        self._notifier = can.Notifier(bus, [self._listener], loop=loop) 

    def __del__(self):
        self.stop()

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self._listener.get_message()
        log.debug(msg)
        if not msg:
           raise StopAsyncIteration
        else:
            return msg

    async def get_message(self):
        msg = await self._listener.get_message()
        log.debug(msg)
        return msg

    def stop(self):
        log.debug('canreader stopping')
        try:
            self._notifier.stop()
        except Exception as e:
            log.warning(e)
