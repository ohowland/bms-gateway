""" Gateway reads, translates, and writes CANbus frames.

    Author: Owen Edgerton
    For: Howl & Edgerton, LLC
    Date: 8/15/20
"""

import asyncio
import logging
import time

from target import Target
from translator import Translator

LOGGER = logging.getLogger('gateway')

async def bms_target(target, queue):
    """ the bms_target loop reads the bms CANbus and enques information
        for the translation loop.
    """

    while True:
        msg = await target.read_canbus()
        if msg:
            target.update_status(msg)
            await queue.put(msg)

async def translation_loop(translator, in_queue, out_queue):
    """ the translation loop facilitates mapping of incoming data
        to outgoing data
    """

    while True:
        msg = await in_queue.get()
        translated_msg = translator.translate(msg)
        await out_queue.put(translated_msg)

async def inv_target(target, queue):
    """ the inv_target loop continiously writes the inverter canbus
    """

    # these values do not have a corresponding Nuvation BMS register.
    # they are initialized to zero at the start of this loop.
    static = {
        "IO_STATE": {
            "IO_STATE_SOH": 100
        },
        "IO_ALARM": {
            "IO_ALARM_SHORT_ARRIVE": 0,
            "IO_ALARM_SHORT_LEAVE": 0,
            "IO_WARN_SHORT_ARRIVE": 0,
            "IO_WARN_SHORT_LEAVE": 0,
            "IO_ALARM_CELL_IMBAL_ARRIVE": 0,
            "IO_ALARM_CELL_IMBAL_LEAVE": 0,
            "IO_WARN_CELL_IMBAL_ARRIVE": 0,
            "IO_WARN_CELL_IMBAL_LEAVE": 0,
        },
    }
    target.update_control(static)

    while True:
        msg = await queue.get()
        if msg:
            target.update_control(msg)
            if target.ready():
                for msg in target.get_write_buffer():
                    target.write_canbus(msg)

def main(**kwargs):
    """ start the BMS-SMA gateway
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
    except Exception as error:
        LOGGER.fatal("system crash %s", error)
        loop.close()

if __name__ == '__main__':
    pass
