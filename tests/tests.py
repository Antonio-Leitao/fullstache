import sys

sys.path.append("fullstache")

import unittest
from interpreter import Fullstache


class TestInterpreter(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data = {
            "name": {"first": "MIKE", "last": "SHINODA"},
            "exists": "True",
            "persons": [{"age": 12}, {"age": 44}],
            "money": 32,
            "bool": {"variable": "True"},
        }
        self.fullstache = Fullstache()

    def test_substitution(self):
        doc = """{{name.first}}"""
        result = self.fullstache.interpret(doc, self.data)
        self.assertEqual(result, self.data["name"]["first"])

    def test_noVariables(self):
        doc = """{This is a random text <<z<<>dsa //8211??!!"""
        result = self.fullstache.interpret(doc, self.data)
        self.assertEqual(result, doc)

    def test_cleaning(self):
        doc = "{{name.last}} something here though {{name.first}} and here"
        result = self.fullstache.interpret(doc, self.data)
        self.assertEqual(result, "SHINODA something here though MIKE and here")


if __name__ == "__main__":
    unittest.main()
