""" Copywrite: Howl & Edgerton, LLC 8/21/2020
    Author: Owen Edgerton
    Name: can_reader.py
    Description:
"""

import logging

import can

LOGGER = logging.getLogger('can_reader')

class CANReader:
    """ CANReader creates an access point for asynchronously reading from a CAN bus.

    """
    def __init__(self, bus, loop):
        self._listener = can.AsyncBufferedReader()
        self._notifier = can.Notifier(bus, [self._listener], loop=loop)

    def __del__(self):
        self.stop()

    def __aiter__(self):
        return self

    async def __anext__(self):
        msg = await self._listener.get_message()
        LOGGER.debug(msg)
        if not msg:
            raise StopAsyncIteration

        return msg

    async def get_message(self):
        """ get_message awaits and returns the next message on the CANbus
        """

        msg = await self._listener.get_message()
        LOGGER.debug(msg)
        return msg

    def stop(self):
        """ stop disconnects this routine from the can bus
            it cannot be started again
        """

        LOGGER.debug('canreader stopping')
        try:
            self._notifier.stop()
        except can.CanError as error:
            LOGGER.warning("CANreader encountered exception while stopping %s", error)
