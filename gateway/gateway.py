""" Name: gateway.py
    Author: Howl & Edgerton, llc 2020
    About: Nuvation BMS to SMA Sunny Island Gateway.
"""

import asyncio
import os
import logging

from can_writer import CANWriter
from can_target_inverter import SMA
from can_target_bms import Nuvation

from datetime import datetime
from configparser import ConfigParser
from datetime import datetime
from collections import namedtuple

async def poll_target(poller, target, queue):
    """ The poll_target loop continiously polls configured objects
        and pipes ---.
    """

    while True:
        print('Polling Target @ {}'.format(datetime.now().time()))

        response = poller.read(target.comm.registers)
        print("response: {}".format(response))
        target.update_from(response)


        if response:
            await queue.put(response)
        # pipe data can writer
        await asyncio.sleep(poller.update_rate)

async def write_bus(writer, target, queue):
    """ The update loop continiously writes the canbus
    """

    while True:
        data = await queue.get()
        print('Writing CAN bus @ {}'.format(datetime.now().time()))
        target.update_messages(data)
        print("Messages: {}\nSignals: {}".format(target.messages, target.signals))

        # Update tasks by message
        #writer.update(target.messages)

def main(*args, **kwargs):
    """ 
    """

    loop = asyncio.get_event_loop()
    bootstrap_config = kwargs['bootstrap']

    poller = ModbusPoller(bootstrap_config['BMS_COMM'])
    modbus_target = Nuvation()
    writer = CANWriter(bootstrap_config['INV_COMM'])
    canbus_target = SMA(bootstrap_config['INV_COMM'])

    queue = asyncio.Queue(maxsize=1, loop=loop)

    loop.create_task(poll_target(poller, modbus_target, queue))
    loop.create_task(write_bus(writer, canbus_target, queue))

    try:
        loop.run_forever()
    except:
        loop.close()