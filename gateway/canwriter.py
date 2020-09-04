""" Name: can_writer.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging

LOGGER = logging.getLogger('sys')

class CANWriter:
    ''' CANWriter controls the publishing of periodic messages on the
        CANbus resource
    '''


    def __init__(self, config, bus):
        self._bus = bus
        self._update_rate = float(config['update_rate'])
        self._tasks = {}

    def publish(self, name, msg):
        ''' iterate messages, check if a task is to be created or modified
        '''
        task = self._tasks.get(name, None)
        if task:
            task.modify_data(msg)
        else:
            task = self._bus.send_periodic(msg, self._update_rate)
            self._tasks.update({name: task})

    def stop(self):
        ''' stop shuts down all tasks (send_periodic) spawned by the
            CANWriter
        '''

        LOGGER.debug("canwriter stoppping")
        for task in self._tasks.values():
            try:
                task.stop()
            except Exception as error:
                LOGGER.warning(error)
