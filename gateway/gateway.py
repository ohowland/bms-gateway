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

async def bms_target(target, queue):
    """ The bms_target loop continiously the bms canbus and enques information
        on the linking queue.
    """
    logger = logging.getLogger('bms')

    cnt = 0
    n = 10 
    t_arr = [0]*n
    while True:
        t0 = time.time()

        target.update_status()
        await queue.put(target.status)

        t1 = time.time()
        t_arr[cnt] = t1-t0
        cnt = (cnt + 1) % n
        if cnt == n-1:
            logger.debug("bms avg loop time: {}".format(sum(t_arr)/n))
        

async def inv_target(target, adapter, queue):
    """ The update loop continiously writes the canbus
    """
    
    logger = logging.getLogger('inv')

    cnt = 0
    n = 10
    t_arr = [0]*n
    while True:
        t0 = time.time()

        data = await queue.get()
        if data:
            logging.debug(data)
        target.write_control()

        t1 = time.time()
        t_arr[cnt] = t1-t0
        cnt = (cnt + 1) % n
        if cnt == n-1:
            logger.debug("inv avg loop time: {}".format(sum(t_arr)/n))

def main(*args, **kwargs):
    """ 
    """

    loop = asyncio.get_event_loop()
    bootstrap_config = kwargs['bootstrap']

    bms = Target(bootstrap_config['BMS_COMM'])
    inv = Target(bootstrap_config['INV_COMM'])

    adapter = None 

    queue = asyncio.Queue(maxsize=1, loop=loop)

    loop.create_task(bms_target(bms, queue))
    loop.create_task(inv_target(inv, adapter, queue))

    try:
        loop.run_forever()
    except:
        loop.close()
