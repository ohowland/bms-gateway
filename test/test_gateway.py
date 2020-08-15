import unittest
from configparser import ConfigParser

from .context import config, target

class TestGateway(unittest.TestCase):

    def setUp(self):
        bootstrap_parser = ConfigParser()
        bootstrap_path = config.get('bootstrap.ini', TESTING=True)
        bootstrap_parser.read(bootstrap_path.as_posix())
        self.inv_config = bootstrap_parser['INV_COMM']
        self.bms_config = bootstrap_parser['BMS_COMM']

        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue(maxsize=10, loop=self.loop)

    def tearDown(self):
        pass

    def test_queue_transfer(self):

        task_inv = loop.create_task(inv_target(self.inv_config, self.queue))
        task_bms = loop.create_task(bms_target(self.bms_config, self.queue))

     
    async def bms_target(target, queue):
    """ The bms_target loop continiously the bms canbus and enques information
    on the linking queue.
    """
        while True:
            msg = target.read_canbus()
            await queue.put(msg)
            break

    async def inv_target(target, queue):
        """ The update loop continiously writes the canbus
        """
        
        while True:
            data = await queue.get()
            self.assertIs(data)
            log.debug(data)
            break
