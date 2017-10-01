import unittest
from configparser import AbstractConfigParser, JSONConfigParser


class TestConfigParser(unittest.TestCase):
    def test_00(self):
        """
        Init
        """
        self.assertIsInstance(JSONConfigParser(), AbstractConfigParser)
        with self.assertRaises(TypeError):
            AbstractConfigParser()

    def test_01(self):
        op_key, template = JSONConfigParser().parse({
            "__OP_KEY__": "ops",
            "template": '''{
                "user": {
                    "name": "delete",
                    "password": {"ops":""}
                }
            }'''})
        self.assertEqual(op_key, 'ops')
