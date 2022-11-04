from lark import Transformer
from lark.visitors import Interpreter, Visitor_Recursive
from functools import reduce  # forward compatibility for Python 3
from operator import getitem
from lark import Lark, Tree
from loaders import loadParser


def getFromDict(dataDict, mapList):
    return reduce(getitem, mapList, dataDict)


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


class FullstacheError(Exception):
    pass


class Fullstache(Transformer):
    def __init__(self, user_data):
        self.data = user_data

    def JUNK(self, child):
        return child[3:-3]

    def VARIABLE(self, child):
        try:
            var = getFromDict(self.data, child.split("."))
            var = Variable(value=var, template=child, exists=True)
        except KeyError:
            var = Variable(value=None, template=child, exists=False)
        return var

    def NUMBER(self, child):
        return float(child)

    def start(self, children):
        flat = [item for child in children for item in child]
        return "".join(flat)

    def bool_neg(self, child):
        return not child[0]

    def bool_and(self, children):
        a, b = children
        return a and b

    def bool_or(self, children):
        a, b = children
        return a or b

    def equal(self, children):
        a, b = children
        return a == b

    def nequal(self, children):
        a, b = children
        return a != b

    def arith_big(self, children):
        a, b = children
        return float(a) > float(b)

    def arith_less(self, children):
        a, b = children
        return float(a) < float(b)

    def arith_beq(self, children):
        a, b = children
        return float(a) >= float(b)

    def arith_leq(self, children):
        a, b = children
        return float(a) <= float(b)

    def arith_add(self, children):
        a, b = children
        return float(a) + float(b)

    def arith_sub(self, children):
        a, b = children
        return float(a) - float(b)

    def arith_mul(self, children):
        a, b = children
        return float(a) * float(b)

    def arith_div(self, children):
        a, b = children
        return float(a) / float(b)

    def arith_neg(self, child):
        return not child

    def ifelse(self, children):
        if children[0]:
            return children[1]
        elif len(children) > 2:
            return children[2]
        return ""

    def iterator(self, children):
        n = len(children[0])
        return children[1:] * n


class Compiler(Interpreter):
    def enumerator(self, nodes):
        print("ENUM:", nodes)
        return nodes


def collapse(text, data):
    parser = loadParser()
    tree = parser.parse(text)
    # t = Tree("a", [Tree("b", []), Tree("c", []), "d"])

    print(list(Compiler().visit_topdown(tree)))
    pass
