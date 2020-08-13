""" Name: gateway.py
    Author: Howl & Edgerton, llc 2020
    About: Nuvation BMS to SMA Sunny Island Gateway.
"""

import asyncio
import os
import logging
import time

from target import Target
from configparser import ConfigParser

class timer

async def bms_target(target, queue):
    """ The bms_target loop continiously the bms canbus and enques information
        on the linking queue.
    """

    while True:
        msg = target.read_canbus()
        target.update_status(msg)
        await queue.put(msg)

async def inv_target(target, adapter, queue):
    """ The update loop continiously writes the canbus
    """

    log = logging.getLogger('inv')
    while True:
        data = await queue.get()
        if data:
            log.debug(data)
            target.update_control(msg)
            target.write_canbus(msg)

def main(*args, **kwargs):
    """ 
    """

    loop = asyncio.get_event_loop()
    bootstrap_config = kwargs['bootstrap']

    bms = Target(bootstrap_config['BMS_COMM'])
    inv = Target(bootstrap_config['INV_COMM'])

    queue = asyncio.Queue(maxsize=10, loop=loop)

    task_bms = loop.create_task(bms_target(bms, queue))
    task_inv = vloop.create_task(inv_target(inv, queue))

    try:
        loop.run_forever()
    except:
        task_bms.cancel()
        task_inv.cancel()
        loop.close()
