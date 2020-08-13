""" Name: can_writer.py
    Author: Howl & Edgerton, llc 2020
    About:
"""

import logging
import can
import cantools

log = logging.getLogger('sys')

class CANWriter(object):       
    def __init__(self, config, bus):
        self._bus = bus
        self._update_rate = float(config['update_rate'])
        self._tasks = {}

    def __del__(self):
        self.stop()

    def publish(self, name, msg):
        ''' iterate messages, check if a task is to be created or modified 
        '''
        task = self._tasks.get(name, None)
        if task:
            task.modify_data(msg)
        else:
            log.debug("new task created {}".format(name))
            task = self._bus.send_periodic(msg, self._update_rate)
            self._tasks.update({name: task})

    def stop(self):
        for task in self._tasks.values():
            try:
                task.stop()
            except Exception as e:
                log.warning(e)
                

