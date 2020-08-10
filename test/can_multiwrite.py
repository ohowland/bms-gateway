#!/usr/bin/env python3

import logging
import time
import asyncio

import can

from pymodbus.client.asynchronous.tcp import AsyncModbusTCPClient as ModbusClient
from pymodbus.client.asynchronous import schedulers

from threading import Thread

logging.basicConfig(level=logging.INFO)

''' Two loops, a modbus read and a client write.
    Data is read over modbus from BMS, transformed,
    mapped to CAN registers, and written to the CAN bus.

    Two async loops are spun up for communication.
    1. Data received on a modbus read.
    2. Data is written on a can write.

    modbus data decoded and put into dict[string] value.
    
    some function maps modbus register values to can
    register values.

    can register dict[string]value

    can data encoded to bytes for can.Message class
    can task is updated with current can.Message data.
'''

async def read_modbus_client(client):
    logging.debug('Starting periodic Modbus client poll')
    # Configure holding register reads
    # get a decoder -> dict[string]value
    
    data_model = dict()
    while True:
        UNIT = 0x01
        resp = await client.read_holding_registers(1, 8, unit=UNIT)
        data_model.update(decode_modbus(resp))
        await asyncio.sleep(0.5)
        
    logging.debug('Stopping periodic Modbus client poll')

def decode_modbus(resp) -> dict:
    return dict()

async def write_can_bus(bus):
    logging.debug('Starting periodic CAN bus write')
    msg = can.Message(
        arbitration_id=0x321, 
        data=[0xB, 0xE, 0xE, 0xF], 
        is_extended_id=False
    )
    task = bus.send_periodic(msg, 0.2)
    assert isinstance(task, can.ModifiableCyclicTaskABC)

    while True:
        # read latest msg values from dict[string]value
        # encode values to msg.data
        msg.data = [1, 0, 0, 0]
        task.modify_data(msg)

        await asyncio.sleep(0.1)
    task.stop()
    logging.debug('Stopping periodic CAN bus write')

def print_message(msg):
    print(msg)

if __name__ == '__main__':

    # create channel
    # launch async modbus read
    # launch async can send 
    
    can0 = can.Bus('vcan0', bustype='virtual', receive_own_messages=True)

    logging.debug('Starting Async Loop')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    #client = ModbusClient(schedulers.ASYNC_IO, port=5020, loop=loop)

    
    loop.run_forever()
    loop.close()
