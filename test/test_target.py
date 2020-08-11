import logging
import unittest
from pathlib import Path
from configparser import ConfigParser

import cantools

from gateway import config, translator 


class TestTarget(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.bootstrap = bootstrap_parser

    def tearDown(self):
        pass

    def test_update_status(self):
        

