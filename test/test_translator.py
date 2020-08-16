import unittest

from .context import Translator

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.t = Translator()

    def tearDown(self):
        pass

    def translate_single_msg_single_signal(self):
        t = Translator()

        msg = {'IO_STACK_V': {'IO_STACK_V': 45}}
        t_msg = t.translate(msg)

        assertedMsg = {"IO_STATUS": {"IO_STATUS_V": 45}}
        self.assertEqual(t_msg, assertedMsg)

    def translate_single_msg_multi_signal(self):
        t = Translator()

        msg = {'IO_STACK_V': {'IO_STACK_V': 45}, "IO_STACK_I": {"IO_STACK_I": 200}}
        t_msg = t.translate(msg)

        assertedMsg = {"IO_STATUS": {"IO_STATUS_V": 45, "IO_STATUS_I": 200}}
        self.assertEqual(t_msg, assertedMsg)
        