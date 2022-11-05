"""fullstache main class

ACCEPTS: parser and compiler
SPITS: fullstache class 
"""

from .parser import Parser
from .compiler import Compiler


class Fullstache:
    def __init__(self, user_data=None):
        self.parser = Parser()
        self.compiler = Compiler(user_data)

    def interpret(self, doc, data):
        tree = self.parser.parse(doc)
        if tree is None:
            return doc
        result = self.compiler.compile(tree)
        return result

    def scan(self, dir):
        pass
