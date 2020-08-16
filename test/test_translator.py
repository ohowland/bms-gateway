import unittest

from .context import translator

class TestTranslator(unittest.TestCase):
    def setUp(self):
        self.t = translator.Translator()

    def tearDown(self):
        pass

    def test_translate_single_msg_single_signal(self):

        msg = {"IO_STACK_V": {"IO_STACK_V": 45}}
        t_msg = self.t.translate(msg)

        assertedMsg = {"IO_STATUS": {"IO_STATUS_V": 45}}
        self.assertEqual(t_msg, assertedMsg)

    def test_translate_single_msg_multi_signal(self):
        msg = {"IO_STACK_V": {"IO_STACK_V": 45}, "IO_STACK_I": {"IO_STACK_I": 200}}
        t_msg = self.t.translate(msg)

        assertedMsg = {"IO_STATUS": {"IO_STATUS_V": 45, "IO_STATUS_I": 200}}
        self.assertEqual(t_msg, assertedMsg)
    
    def test_translate_multimap(self):
        msg = {"IO_SOC": {"IO_SOC": 0.62}}
        t_msg = self.t.translate(msg)

        assertedMsg = {"IO_STATE": {"IO_STATE_SOC": 0.62, "IO_STATE_SOC_HIRES": 0.62}}
        self.assertEqual(t_msg, assertedMsg)
