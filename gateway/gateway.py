""" Gateway reads, translates, and writes CANbus frames.

    Author: Owen Edgerton 
    For: Howl & Edgerton, LLC 
    Date: 8/15/20
"""

import asyncio
import os
import logging
import time
import signal

from target import Target
from translator import Translator
from configparser import ConfigParser

log = logging.getLogger('inv')

async def bms_target(target, queue):
    """ The bms_target loop continiously the bms canbus and enques information
        for the translation loop
    """

    while True:
        try:
            msg = await target.read_canbus()
            if msg:
                target.update_status(msg)
                await queue.put(msg)
        except Exception as e:
            log.warning(e)

async def translation_loop(t, in_queue, out_queue):
    """ the translation loop facilitates mapping of incoming data 
        to outgoing data
    """

    while True:
        msg = await in_queue.get()
        translated_msg = t.translate(msg)
        await out_queue.put(translated_msg)

async def inv_target(target, queue):
    """ the inv_target loop continiously writes the inverter canbus
    """

    while True:
        try:
            msg = await queue.get()
            if msg:
                log.debug(msg)
                target.update_control(msg)
        
            for msg in target.get_write_buffer():
                target.write_canbus(msg)
        except Exception as e:
            log.warning(e)

def main(*args, **kwargs):
    """ 
    """

    loop = asyncio.get_event_loop()
    config = kwargs['bootstrap']

    bms = Target(config['BMS_COMM'], loop)
    bms_queue = asyncio.Queue(maxsize=10, loop=loop)
    loop.create_task(bms_target(bms, bms_queue))

    inv = Target(config['INV_COMM'], loop)
    inv_queue = asyncio.Queue(maxsize=10, loop=loop)
    loop.create_task(inv_target(inv, inv_queue))

    translator = Translator()
    loop.create_task(
        translation_loop(translator, in_queue=bms_queue, out_queue=inv_queue) 
    )

    try:
        loop.run_forever()
    except:
        loop.close()
