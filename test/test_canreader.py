import logging
import unittest
import can
import time
import asyncio

from .context import config, canreader

from pathlib import Path
from configparser import ConfigParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestCANReader(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser
        loop = asyncio.get_event_loop()

    def tearDown(self):
        pass

    def test_config(self):
        reader = canreader.CANReader(self.bootstrap['BMS_COMM'])

        self.assertEqual(reader.interface, "virtual")
        self.assertEqual(reader.channel, "vcan1")
        self.assertEqual(reader.baudrate, "500000")

    async def test_reader(self):
        bus = can.interface.Bus("vcan1", bustype="virtual")

        reader = canreader.CANReader(self.bootstrap['BMS_COMM'], loop=loop)
        
        test_msg = can.Message(arbitration_id = 0x321,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg)

        resp = await reader.get_message()

        self.assertEqual(resp.data, test_msg.data)
        self.assertEqual(resp.arbitration_id, test_msg.arbitration_id)

        reader.stop()
    
    async def test_reader_one_can_id(self):
        bus = can.interface.Bus("vcan1", bustype="virtual")
        reader = canreader.CANReader(self.bootstrap['BMS_COMM'], loop=loop)
        
        test_msg1 = can.Message(arbitration_id = 0x321,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg1)

        test_msg2 = can.Message(arbitration_id = 0x321,
                                data = [0xCA, 0xFE, 0x12, 0x34],
                                is_extended_id = False) 
        bus.send(test_msg2)

        resp = await reader.get_message()
        self.assertEqual(resp.data, test_msg1.data)
        self.assertEqual(resp.arbitration_id, test_msg1.arbitration_id)
        
        resp = await reader.get_message()
        self.assertEqual(resp.data, test_msg2.data)
        self.assertEqual(resp.arbitration_id, test_msg2.arbitration_id)

        reader.stop()
    
    async def test_multi_reader_multi_can_ids(self):
        bus = can.interface.Bus("vcan1", bustype="virtual")
        
        reader = canreader.CANReader(self.bootstrap['BMS_COMM'], loop=loop)
        
        test_msg1 = can.Message(arbitration_id = 0xABC,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg1)

        test_msg2 = can.Message(arbitration_id = 0xDEF,
                                data = [0xCA, 0xFE, 0x12, 0x34],
                                is_extended_id = False) 
        bus.send(test_msg2)

        resp = await reader.get_message()
        self.assertEqual(resp.data, test_msg1.data)
        self.assertEqual(resp.arbitration_id, test_msg1.arbitration_id)
        
        resp = await reader.get_message()
        self.assertEqual(resp.data, test_msg2.data)
        self.assertEqual(resp.arbitration_id, test_msg2.arbitration_id)

        reader.stop()

    async def test_iterator(self):
        bus = can.interface.Bus("vcan1", bustype="virtual")
        reader = canreader.CANReader(self.bootstrap['BMS_COMM'], loop=loop)
        
        test_msg = can.Message(arbitration_id = 0xABC,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg)

        test_msg = can.Message(arbitration_id = 0xABC,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg)
        
        test_msg = can.Message(arbitration_id = 0xABC,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        bus.send(test_msg)

        
        for msg in reader:
            self.assertEqual(msg.data, test_msg.data)
            self.assertEqual(msg.arbitration_id, test_msg.arbitration_id)

        reader.stop()
