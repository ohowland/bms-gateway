import unittest
import time
from configparser import ConfigParser

import cantools

from gateway import config
from target import Target


class TestTarget(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_write_control(self):
        sma = Target(self.bootstrap['INV_COMM'])

        test_name = 'IO_STATE'
        test_data = {'IO_STATE_SOC': 67,
                'IO_STATE_SOH': 98,
                'IO_STATE_SOC_HIRES': 67.14}

        sma._control.update({test_name: test_data})
        
        sma.write_control()
        time.sleep(0.5)
        sma.update_status()

        self.assertEqual(test_data, sma._status[test_name])

        sma.stop()


        

