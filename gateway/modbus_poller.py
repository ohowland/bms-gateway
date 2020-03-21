""" Name: poller.py
    Author: Howl & Edgerton, llc 2020
    About: Communications module
"""
import logging

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

from configparser import ConfigParser
from collections import namedtuple, OrderedDict


class Modbus(object):
    register = namedtuple(
        'modbus_register', 'name, address, type, function_code')

    def __init__(self):
        pass


class ModbusPoller(Modbus):

    def __init__(self, config):
        self.ip_addr = config['ip_addr']
        self.id = int(config['modbus_id'])
        self.port = int(config['port'])
        self.update_rate = int(config['update_rate'])
        self.endian = self.endian_helper(config['endian'])
        self.offset = int(config['offset'])

    def read(self, registers):
        print("polling: {}".format(self.ip_addr))
        try:
            client = ModbusTcpClient(self.ip_addr, port=self.port)

            response = {}
            for register in registers:
                incoming = client.read_holding_registers(
                    register.address + self.offset,
                    count=self.size_of(register.type),
                    unit=self.id)
                print(incoming)
                result = self.decode(incoming, register.type)

                response.update({register.name: result})

            client.close()
            return response

        except:
            return {}

    def endian_helper(self, endian_string):
        if endian_string.lower == "little":
            return Endian.Little
        return Endian.Big

    # TODO: Implement more datatypes
    def decode(self, incoming, type):
        decoder = BinaryPayloadDecoder.fromRegisters(
            incoming.registers,
            byteorder=self.endian,
            wordorder=self.endian
        )

        if type == 'U16':
            return decoder.decode_16bit_uint()
        elif type == 'I16':
            return decoder.decode_16bit_int()
        elif type == 'U32':
            return decoder.decode_32bit_uint()
        elif type == 'I32':
            return decoder.decode_32bit_int()
        elif type == 'F32':
            return decoder.decode_32bit_float()

        return 0

    # TODO: Implement more datatypes
    def size_of(self, type):
        if type == 'U16' or 'I16':
            return 1
        elif type == 'U32' or 'I32' or 'F32':
            return 2
        else:
            return 0