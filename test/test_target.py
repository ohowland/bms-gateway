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
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_write_control(self):
        inv = target.Target(self.bootstrap['INV_COMM'])

        test_name = 'IO_STATE'
        test_data = {'IO_STATE_SOC': 67,
                'IO_STATE_SOH': 98,
                'IO_STATE_SOC_HIRES': 67.14}

        inv._control.update({test_name: test_data})
        
        inv.write_control()
        time.sleep(0.5)
        resp = inv.update_status()

        self.assertEqual(test_data, resp[test_name])

        inv.stop()

    def test_update_status(self):
        loop = asyncio.get_event_loop()

        inv = target.Target(self.bootstrap['INV_COMM'], loop=loop)
        bms = target.Target(self.bootstrap['BMS_COMM'], loop=loop)

        queue = asyncio.Queue(maxsize=20, loop=loop)
        
        loop.create_task(bms_target(bms, queue))
        loop.create_task(inv_target(inv, queue))

        loop.run_forever()    

async def bms_target(target, queue):
    while True:
        data = target.update_status()
        print("sending:", data)
        await queue.put(data)

async def inv_target(target, queue):
    while True:
        data = await queue.get()
        print("recieved:", data)
        target.write_control(data)



