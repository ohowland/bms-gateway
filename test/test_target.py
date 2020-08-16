import unittest
import time
import asyncio

from configparser import ConfigParser

import can

from .context import config, target

class TestTarget(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.config = bootstrap_parser
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        pass

    def test_write_canbus(self):
        self.loop.run_until_complete(
            asyncio.gather(self._test_write_canbus())
        )

    async def _test_write_canbus(self):
        inv = target.Target(self.config['INV_COMM'], self.loop)

        test_name = 'IO_STATE'
        test_data = {
                'IO_STATE_SOC': 67,
                'IO_STATE_SOH': 98, 
                'IO_STATE_SOC_HIRES': 67.14,
        } 
        
        inv.write_canbus({test_name: test_data})

        resp = await inv.read_canbus()

        for _, data in resp.items():
            self.assertEqual(data, test_data)

    def test_queue_pass(self):
        self.loop.run_until_complete(
            asyncio.gather(self._test_queue_pass())
        )

    async def _test_queue_pass(self):
        inv = target.Target(self.config['INV_COMM'], self.loop)
        bms = target.Target(self.config['BMS_COMM'], self.loop)

        queue = asyncio.Queue(maxsize=20, loop=self.loop)
        
        self.loop.create_task(inv_target(inv, queue))
        self.loop.create_task(bms_target(bms, queue))

async def bms_target(target, queue):
    test_name = 'IO_STATE'
    test_data = {
                'IO_STATE_SOC': 67,
                'IO_STATE_SOH': 98, 
                'IO_STATE_SOC_HIRES': 67.14,
    } 
    while True:
        data = {test_name, test_data}
        print("sending:", data)
        await queue.put(data)
        break

async def inv_target(target, queue):
    while True:
        data = await queue.get()
        print("recieved:", data)
        break
