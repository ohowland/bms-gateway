import logging
import unittest
import can

from gateway import config
from gateway.can_writer import CANWriter
from gateway.can_target import SMA


from pathlib import Path
from configparser import ConfigParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestCANWriter(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        writer = CANWriter(self.bootstrap['SMA_COMM'])
        self.assertEqual(writer.interface, "virtual")
        self.assertEqual(writer.channel, "vcan0")
        self.assertEqual(writer.baudrate, "500000")

    def test_write(self):
        testbus = can.interface.Bus("vcan0", bustype="virtual", receive_own_messages=True)

        writer = CANWriter(self.bootstrap['SMA_COMM'])
        test_msg = {'IO_SOC': 1, 'IO_VPACK': 2}
        #writer.update(test_msg)

        #resp = testbus.recv()
        #self.assertEqual(test_msg, resp)


class TestCANTarget(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_config(self):
        sma = SMA(self.bootstrap['SMA_DBC'])
        # how to check db loaded?

    def test_encode_decode_soc(self):
        sma = SMA(self.bootstrap['SMA_DBC'])
        test_msg = {'IO_SOC': 1, 'IO_VPACK': 2}
        batt_state_msg = sma.comm.db.get_message_by_name('BATT_STATE')
        data = batt_state_msg.encode(test_msg)
        batt_state_msg.data = data
        decoded = sma.comm.db.decode_message(batt_state_msg.frame_id,  batt_state_msg.data)
        self.assertEqual(decoded, test_msg)

    def test_get_signals(self):
        sma = SMA(self.bootstrap['SMA_DBC'])
        #logging.debug("signals {}".format(sma.signals))
        test_msg = {'IO_SOC': 1, 'IO_VPACK': 2}
        sma.update_messages(test_msg)
        #logging.debug("messages {}".format(sma.messages))

class TestCAN(unittest.TestCase):
    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.CANWriter = CANWriter(bootstrap_parser['SMA_COMM'])
        self.CANTarget = SMA(bootstrap_parser['SMA_DBC'])

