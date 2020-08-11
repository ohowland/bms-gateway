#!/usr/bin/env/ python3

import asyncio
import logging
import time

import can

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    bus = can.Bus('vcan0', bustype='socketcan')
    logging.debug('starting can bus writer')
    
    msg = can.Message(
            arbitration_id=0x321,
            data=[0xB, 0xE, 0xE, 0xF],
            is_extended_id=False
            )
    
    logging.debug('data: {}'.format(msg.data))

    task = bus.send(msg)

    logging.debug('msg sent')

    '''
    loop = asyncio.get_event_loop()

    loop.run_until_complete(write_can_bus(can0))
    loop.close()
    '''
