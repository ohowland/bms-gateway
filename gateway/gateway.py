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
        on the linking queue.
    """

    while True:
        msg = target.read_canbus()
        target.update_status(msg)
        await queue.put(msg)

async def inv_target(target, queue):
    """ The update loop continiously writes the canbus
    """

    while True:
        data = await queue.get()
        if data:
            log.debug(data)
            target.update_control(data)
            target.write_canbus(data)

async def translation_loop(t, in_queue, out_queue):
    while True:
        msg = await in_queue.get()
        translated_msg = t.translate(msg)
        await out_queue.put(translated_msg)

def main(*args, **kwargs):
    """ 
    """

    loop = asyncio.get_event_loop()
    config = kwargs['bootstrap']

    bms = Target(config['BMS_COMM'], loop)
    bms_queue = asyncio.Queue(maxsize=10, loop=loop)
    loop.create_task(bms_target(bms, bms_queue), name="bms_target")

    inv = Target(config['INV_COMM'], loop)
    inv_queue = asyncio.Queue(maxsize=10, loop=loop)
    loop.create_task(inv_target(inv, inv_queue), name="inv_target")

    translator = Translator(config['BMS_COMM'], config['INV_COMM'])
    loop.create_task(
        translation_loop(translator, in_queue=bms_queue, out_queue=inv_queue),
        name="translator"
    )

    try:
        loop.run_forever()
    except:
        loop.close()