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
        self.config = bootstrap_parser['INV_COMM']

        self.bus = can.interface.Bus(
            self.config['channel'],
            bustype=self.config['interface'],
            bitrate=self.config['baudrate'],
        )
        
    def tearDown(self):
        pass

    def test_reader(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            asyncio.gather(self._test_reader())
        )

    async def _test_reader(self):
        self.bus.flush_tx_buffer()
        reader = canreader.CANReader(self.config, self.bus, self.loop)

        test_msg = can.Message(arbitration_id = 0x321,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        
        task = self.bus.send_periodic(test_msg, float(self.config['update_rate']))
        resp = await reader.get_message()
        task.stop()
        
        self.assertEqual(resp.data, test_msg.data)
        self.assertEqual(resp.arbitration_id, test_msg.arbitration_id)

        reader.stop()

    def test_reader_one_can_id(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            asyncio.gather(self._test_reader_one_can_id())
        )
    
    async def _test_reader_one_can_id(self):
        self.bus.flush_tx_buffer()
        reader = canreader.CANReader(self.config, self.bus, self.loop)
        
        test_msg1 = can.Message(arbitration_id = 0x321,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        
        task1 = self.bus.send_periodic(test_msg1, .5)

        resp = await reader.get_message()
        task1.stop()

        self.assertEqual(resp.data, test_msg1.data)
        self.assertEqual(resp.arbitration_id, test_msg1.arbitration_id)
        
        test_msg2 = can.Message(arbitration_id = 0x321,
                                data = [0xCA, 0xFE, 0x12, 0x34],
                                is_extended_id = False) 
        
        task2 = self.bus.send_periodic(test_msg2, .5)
        resp = await reader.get_message()
        task2.stop()

        self.assertEqual(resp.data, test_msg2.data)
        self.assertEqual(resp.arbitration_id, test_msg2.arbitration_id)

        reader.stop()

    def test_iterator(self):
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            asyncio.gather(self._test_iterator())
        )
        
    async def _test_iterator(self):
        self.bus.flush_tx_buffer()
        reader = canreader.CANReader(self.config, self.bus, self.loop)
        
        test_msg = can.Message(arbitration_id = 0x321,
                                data = [0xDE, 0xAD, 0xBE, 0xEF],
                                is_extended_id = False) 
        
        task = self.bus.send_periodic(test_msg, .1)

        cnt = 0 
        async for msg in reader:
            self.assertEqual(msg.data, test_msg.data)
            self.assertEqual(msg.arbitration_id, test_msg.arbitration_id)
            cnt += 1
            if cnt > 2:
                break
        else:
            pass

        task.stop()
        reader.stop()
