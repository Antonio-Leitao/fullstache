from lark.visitors import Interpreter, Visitor_Recursive
from parser import buildParser
from functools import reduce  # forward compatibility for Python 3
from operator import getitem
import re


def getFromDict(dataDict, mapList):
    return reduce(getitem, mapList, dataDict)


class FullstacheError(Exception):
    pass


class Variable:
    def __init__(self, value=None, template=None, exists=False):
        self.value = value
        self.template = template
        self.exists = exists
        self.numeric_val = None
        self.bool_val = None

    def __repr__(self):
        if not self.exists:
            raise FullstacheError(
                f"Could not interpret template variable {self.template} from supplied data"
            )
        if type(self.value) == dict or type(self.value) == list:
            return str(self.value)
        return self.value

    def __len__(self):
        if hasattr(self.value, "__len__"):
            return len(self.value)
        else:
            raise FullstacheError(
                f"Could not iterate throught template variable {self.template}."
            )

    def __bool__(self):
        if type(self.value) == bool:
            self.bool_val = self.value
            return self.value
        if not self.exists:
            self.bool_val = False
            return self.bool_val
        if type(self.value) == list and len(self.value) == 0:
            self.bool_val = False
            return self.bool_val
        if type(self.value) == str:
            if self.value in ["False", "false"]:
                self.bool_val = False
                return self.bool_val
            elif self.value in ["True", "true"]:
                self.bool_val = True
                return self.bool_val
        if self.value in [0]:
            self.bool_val = False
            return self.bool_val
        self.bool_val = True
        return self.bool_val

    def __float__(self):
        if type(self.value) == float:
            self.numeric_val = self.value
            return float(self.numeric_val)
        if type(self.value) == int:
            self.numeric_val = self.value
            return float(self.numeric_val)
        if type(self.value) == list:
            self.numeric_val = len(self.value)
        else:
            self.numeric_val = float(self.bool_val)
        return float(self.numeric_val)

    def __int__(self):
        return int(self.numeric_val)

    __nonzero__ = __bool__  # just to make sure it works on python <2


class FullstacheCompiler(Interpreter):
    def __init__(self, user_data):
        self.data = user_data

    def enumerator(self, tree):
        a, b, c = tree.children[:3]
        d = tree.children[3:]
        # var = getFromDict(self.data,tree.children[0].split("."))
        print(f"A:{a}\n")
        print(f"B:{b}\n")
        print(f"C:{c}\n")
        print(f"D:{d}\n")
        self.visit_children(tree)
        return

    def VARIABLE(self, tree):
        print("SUB:", tree)


# the standalone version of this. the main should simply call this dude multiple times
# while starting it only once
class Fullstache:
    def __init__(self, grammar=None):
        ###start parser and read grammar
        self.grammar = grammar
        self.parser = buildParser()

    def interpret(self, text, user_data):
        wrapped_text = self._wrapInverse(text)
        if self.skip:
            return text
        tree = self.parser.parse(wrapped_text)
        result = FullstacheCompiler(user_data).visit(tree)
        return result

    def scan(self, doc):
        pass

    def _wrapInverse(self, doc, lwrap="~(~", rwrap="~)~"):
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
