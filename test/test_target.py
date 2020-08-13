import unittest
import time
import asyncio

from configparser import ConfigParser

import cantools

from .context import config, target

class TestTarget(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.config = bootstrap_parser['INV_COMM']
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        pass

    def test_write_canbus(self):
        self.loop.run_until_complete(
            asyncio.gather(self._test_write_canbus())
        )

    async def _test_write_canbus(self):
        inv = target.Target(self.config, self.loop)

        test_name = 'IO_STATE'
        test_data = {'IO_STATE_SOC': 67,
                'IO_STATE_SOH': 98, 'IO_STATE_SOC_HIRES': 67.14} 
        
        inv.write_canbus({test_name: test_data})

'''
    def test_update_status(self):
        loop = asyncio.get_event_loop()
        test(resp)
        inv = target.Target(self.bootstrap['INV_COMM'], loop=loop)
        bms = target.Target(self.bootstrap['BMS_COMM'], loop=loop)

        queue = asyncio.Queue(maxsize=20, loop=loop)
        
        loop.create_task(bms_target(bms, queue))
        loop.create_task(inv_target(inv, queue))

        loop.run_forever()    

def bms_target(target, queue):
    while True:
        data = target.update_status()
        print("sending:", data)
        queue.put_nowait(data)

def inv_target(target, queue):
    while True:
        data = queue.get_nowait()
        print("recieved:", data)
        target.write_control(data)
'''
