"""
ACCEPTS: raw text
SPITS: tree
"""

from lark import Lark
import re

grammar = """
?start:expr*

?expr : "{" "{" "#" VARIABLE "as" VARIABLE ["," VARIABLE] "}" "}" expr* "{""{" "/" "#" "}""}" -> enumerator 
      | "{" "{" VARIABLE "}" "}"
      | JUNK  -> clean


VARIABLE : /[a-zA-Z_$][a-zA-Z_\.0-9]*/
JUNK : /~\(~[\S\s]+?~\)~/ 

%import common.WS
%ignore WS
"""

class Parser:
    def __init__(self):
        self.parser = Lark(grammar)

    def parse(self,doc):
        wrapped_text = self._wrapInverse(doc)
        if self.skip:
            return None
        tree = self.parser.parse(wrapped_text)
        return tree

    def _wrapInverse(self,doc, lwrap="~(~", rwrap="~)~"):
        self.skip = False
        start = 0
        pattern = "\{\{([\S\s]*?)\}\}"
        s = ""
        for match in re.finditer(pattern, doc):
            if match.start() != start:
                s += lwrap + doc[start : match.start()] + rwrap
            s += match.group()
            start = match.end()
        if len(s) == 0:
            self.skip = True
        return s

