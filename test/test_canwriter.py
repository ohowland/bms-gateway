import logging
import unittest
import can
import time

from gateway import config, canwriter

from pathlib import Path
from configparser import ConfigParser

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

class TestCANWriter(unittest.TestCase):

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

    def test_writer(self):
        writer = canwriter.CANWriter(self.config, self.bus)
        msg_name = 'IO_CTRL'
        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)

        resp = self.bus.recv()
        self.assertEqual(msg.data, resp.data)
        self.assertEqual(msg.arbitration_id, resp.arbitration_id)
        
        writer.stop()
    
    def test_multi_writer_one_msg(self):
        writer = canwriter.CANWriter(self.config, self.bus)
        
        msg_name = 'IO_CTRL'
        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)

        msg = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name, msg)
      
        c = 0 
        for msg in self.bus:
            if c == 3:
                break
            self.assertEqual(msg.arbitration_id, 0x321)
            c+=1
        
        writer.stop()
    
    def test_multi_writer_multi_msg(self):
        writer = canwriter.CANWriter(self.config, self.bus)
       
        msg_name1 = 'IO_CTRL'
        msg1 = can.Message(arbitration_id = 0x321,
                               data = [0xDE, 0xAD, 0xBE, 0xEF],
                               is_extended_id = False,
                               timestamp = time.time())
        
        writer.publish(msg_name1, msg1)


        msg_name2 = 'IO_STATE'
        msg2 = can.Message(arbitration_id = 0x305,
                          data = [0xBE, 0xEF, 0xCA, 0xFE],
                          is_extended_id = False,
                          timestamp = time.time())
        
        writer.publish(msg_name2, msg2)

        c = 0
        for msg in self.bus:
            print(msg)
            c += 1
            if c > 3:
                break
            if msg.arbitration_id == 0x321:
                continue
            elif msg.arbitration_id == 0x305:
                continue
            else:
                self.assertTrue(False, "invalid arbitration id on bus")
        
        writer.stop()
